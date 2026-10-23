import datetime
from typing import List, Dict, Any, Optional
from .observability_client import build_client, get_log_group
from .observability_models import LogResponse, LogEvent

SERVICE = "amazon-cloudwatch"

def fetch_recent_logs(start_seconds: int = None, end_seconds: int = None, limit: int = 100) -> List[LogEvent]:
    """Retrieve recent log events filtered by time range.",
    client = build_client(SERVICE)
    response = client.get_log_events(
        logGroupName=get_log_group(),
        logStreamName="structured-logs",
        startTime=start_seconds or int((datetime.datetime.utcnow() - datetime.timedelta(hours=1)).timestamp()),
        endTime=end_seconds or int(datetime.datetime.utcnow().timestamp()),
        limit=limit
    )
    logs: List[LogEvent] = []
    for ev in response.get("events", []):
        # Each event message is a JSON string representing the log event
        try:
            payload = json.loads(ev["message"])
        except json.JSONDecodeError:
            payload = {}
        logs.append(payload)
    return logs