import os
from datetime import datetime, timedelta
from observability_client import get_cloudwatch_client


def fetch_recent_logs(start_time: datetime, end_time: datetime, fields: list = None):
    """Retrieve recent logs filtered by specified time range and optionally fields.
    Returns a list of normalized log events.
    """
    client = get_cloudwatch_client()
    response = client.filter_log_events(
        logGroupName=os.getenv("CLOUDWATCH_LOG_GROUP"),
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
    )
    logs = response.get("events", [])
    normalized = []
    field_set = set(fields) if fields else None
    for event in logs:
        log_data = (
            json.loads(event["message"])
            if isinstance(event["message"], str)
            else event["message"]
        )
        filtered_event = {
            k: v for k, v in log_data.items() if field_set is None or k in field_set
        }
        normalized.append(
            {
                "timestamp": datetime.fromtimestamp(log_data["timestamp"] / 1000),
                **filtered_event,
            }
        )
    return normalized
