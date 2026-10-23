import os
from datetime import datetime, timedelta
from observability_client import get_cloudwatch_client


def query_error_logs(
    start_time: datetime, end_time: datetime, severity_threshold: str = "ERROR"
):
    """Query recent error log entries within a specified time range.
    Returns a list of normalized log events.
    """
    client = get_cloudwatch_client()
    response = client.filter_log_events(
        logGroupName=os.getenv("CLOUDWATCH_LOG_GROUP"),
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        filterPattern=severity_threshold,  # simple filter for severity level
    )
    # Normalize results to a consistent format
    normalized = []
    for event in response.get("events", []):
        log_data = (
            json.loads(event["message"])
            if isinstance(event["message"], str)
            else event["message"]
        )
        normalized.append(
            {
                "timestamp": datetime.fromtimestamp(log_data["timestamp"] / 1000),
                "message": log_data["message"],
                "severity": log_data.get("severity", "INFO"),
                "request_id": log_data.get("request_id"),
            }
        )
    return normalized
