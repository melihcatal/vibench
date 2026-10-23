import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from observability_client import CloudWatchLogsClient, get_time_range
from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    normalize_cloudwatch_event,
)


def fetch_recent_logs(
    minutes_ago: int = 15,
    service: Optional[str] = None,
    component: Optional[str] = None,
    level: Optional[str] = None,
    correlation_id: Optional[str] = None,
    limit: int = 100,
) -> LogQueryResponse:
    client = CloudWatchLogsClient()

    start_time, end_time = get_time_range(minutes_ago)

    filter_parts = []
    if service:
        filter_parts.append(f'$.service = "{service}"')
    if component:
        filter_parts.append(f'$.component = "{component}"')
    if level:
        filter_parts.append(f'$.level = "{level}"')
    if correlation_id:
        filter_parts.append(f'$.correlation_id = "{correlation_id}"')

    if filter_parts:
        filter_pattern = "{" + " && ".join(filter_parts) + "}"
    else:
        filter_pattern = ""

    events = client.filter_log_events(
        filter_pattern=filter_pattern if filter_pattern else None,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return LogQueryResponse(events=events, status="Complete")


def fetch_logs_by_query(
    query_string: str, minutes_ago: int = 15, limit: int = 100
) -> LogQueryResponse:
    client = CloudWatchLogsClient()

    start_time, end_time = get_time_range(minutes_ago)

    query_id = client.start_query(
        query_string=query_string, start_time=start_time, end_time=end_time, limit=limit
    )

    time.sleep(2)

    results = client.get_query_results(query_id=query_id)

    return LogQueryResponse(
        query_id=query_id,
        results=results.get("results", []),
        status=results.get("status", "Unknown"),
    )


def fetch_logs_with_field_value(
    field_name: str, field_value: str, minutes_ago: int = 30, limit: int = 50
) -> List[Dict[str, Any]]:
    query_string = f"""
    fields @timestamp, @message
    | filter {field_name} = "{field_value}"
    | sort @timestamp desc
    | limit {limit}
    """

    response = fetch_logs_by_query(query_string, minutes_ago, limit)

    parsed_logs = []
    for result in response.results:
        log_entry = {}
        for field in result:
            if field.get("field") == "@timestamp":
                log_entry["timestamp"] = field.get("value", "")
            elif field.get("field") == "@message":
                log_entry["message"] = field.get("value", "")
        if log_entry:
            parsed_logs.append(log_entry)

    return parsed_logs


def fetch_logs_by_time_range(
    start_time: datetime,
    end_time: datetime,
    filter_pattern: Optional[str] = None,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    client = CloudWatchLogsClient()

    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(end_time.timestamp() * 1000)

    events = client.filter_log_events(
        filter_pattern=filter_pattern,
        start_time=start_timestamp,
        end_time=end_timestamp,
        limit=limit,
    )

    return events


def fetch_application_logs_summary(minutes_ago: int = 60) -> Dict[str, Any]:
    client = CloudWatchLogsClient()

    start_time, end_time = get_time_range(minutes_ago)

    level_counts = {"INFO": 0, "ERROR": 0, "WARNING": 0, "DEBUG": 0}
    service_counts = {}

    info_logs = fetch_recent_logs(minutes_ago, level="INFO", limit=20)
    error_logs = fetch_recent_logs(minutes_ago, level="ERROR", limit=20)
    warning_logs = fetch_recent_logs(minutes_ago, level="WARNING", limit=20)

    level_counts["INFO"] = len(info_logs.events)
    level_counts["ERROR"] = len(error_logs.events)
    level_counts["WARNING"] = len(warning_logs.events)

    all_logs = info_logs.events + error_logs.events + warning_logs.events

    for event in all_logs:
        try:
            import json

            message = event.get("message", "")
            log_data = json.loads(message)
            service = log_data.get("service", "unknown")
            service_counts[service] = service_counts.get(service, 0) + 1
        except:
            pass

    return {
        "time_range": f"Last {minutes_ago} minutes",
        "total_logs": sum(level_counts.values()),
        "level_distribution": level_counts,
        "service_distribution": service_counts,
        "sample_logs": [
            normalize_cloudwatch_event(event).to_dict() for event in all_logs[:5]
        ],
    }


if __name__ == "__main__":
    recent_logs = fetch_recent_logs(minutes_ago=10, service="api-gateway")
    print(f"Found {len(recent_logs.events)} recent logs from api-gateway")

    summary = fetch_application_logs_summary(minutes_ago=30)
    print(f"Application logs summary: {summary}")

    user_logs = fetch_logs_with_field_value("user_id", "user-12345", minutes_ago=60)
    print(f"Found {len(user_logs)} logs for user-12345")
