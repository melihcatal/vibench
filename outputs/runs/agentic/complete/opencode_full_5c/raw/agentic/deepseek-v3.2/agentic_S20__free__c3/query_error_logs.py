import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from observability_client import CloudWatchLogsClient, get_time_range
from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    normalize_cloudwatch_event,
    create_error_filter_pattern,
)


def query_error_logs(
    minutes_ago: int = 15,
    severity: str = "ERROR",
    service: Optional[str] = None,
    limit: int = 100,
) -> LogQueryResponse:
    client = CloudWatchLogsClient()

    start_time, end_time = get_time_range(minutes_ago)

    filter_pattern = create_error_filter_pattern(level=severity, service=service)

    events = client.filter_log_events(
        filter_pattern=filter_pattern,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return LogQueryResponse(events=events, status="Complete")


def query_errors_with_insights(
    minutes_ago: int = 60, severity: str = "ERROR", service: Optional[str] = None
) -> Dict[str, Any]:
    response = query_error_logs(minutes_ago, severity, service)

    normalized_logs = response.get_normalized_logs()

    error_counts = {}
    services_affected = set()
    error_messages = []

    for log in normalized_logs:
        error_key = f"{log.service}:{log.message[:100]}"
        error_counts[error_key] = error_counts.get(error_key, 0) + 1
        if log.service:
            services_affected.add(log.service)
        error_messages.append(
            {
                "timestamp": log.timestamp,
                "service": log.service,
                "message": log.message,
                "correlation_id": log.correlation_id,
            }
        )

    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    most_common_error = sorted_errors[0] if sorted_errors else None

    return {
        "total_errors": len(normalized_logs),
        "unique_error_types": len(error_counts),
        "services_affected": list(services_affected),
        "most_common_error": {
            "pattern": most_common_error[0] if most_common_error else None,
            "count": most_common_error[1] if most_common_error else 0,
        },
        "time_range": f"Last {minutes_ago} minutes",
        "errors": error_messages[:10],
    }


def query_errors_by_time_window(
    start_time: datetime, end_time: datetime, severity: str = "ERROR"
) -> List[Dict[str, Any]]:
    client = CloudWatchLogsClient()

    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(end_time.timestamp() * 1000)

    filter_pattern = create_error_filter_pattern(level=severity)

    events = client.filter_log_events(
        filter_pattern=filter_pattern,
        start_time=start_timestamp,
        end_time=end_timestamp,
        limit=500,
    )

    return events


def get_error_trend(
    time_intervals: int = 6, interval_minutes: int = 10
) -> List[Dict[str, Any]]:
    trends = []
    end_time = datetime.now()

    for i in range(time_intervals):
        interval_end = end_time - timedelta(minutes=i * interval_minutes)
        interval_start = interval_end - timedelta(minutes=interval_minutes)

        errors = query_errors_by_time_window(interval_start, interval_end)

        trends.append(
            {
                "time_window": f"{interval_start.strftime('%H:%M')} - {interval_end.strftime('%H:%M')}",
                "error_count": len(errors),
                "start_time": interval_start.isoformat(),
                "end_time": interval_end.isoformat(),
            }
        )

    return trends


if __name__ == "__main__":
    errors = query_error_logs(minutes_ago=30, severity="ERROR")
    print(f"Found {len(errors.events)} error logs in last 30 minutes")

    insights = query_errors_with_insights(minutes_ago=60)
    print(f"Error insights: {insights}")

    trend = get_error_trend(time_intervals=4, interval_minutes=15)
    print(f"Error trend: {trend}")
