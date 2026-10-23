import datetime
from typing import List, Dict, Any
from .observability_client import build_client, get_log_group
from .observability_models import LogResponse, ErrorEvent

SERVICE = "amazon-cloudwatch"

def query_error_logs(severity: str = "ERROR", start_seconds: int = None, end_seconds: int = None) -> List[ErrorEvent]:
    """Query recent ERROR (or higher) logs within the supplied time window.",
    # Build filter expression for CloudWatch Logs Insights
    expression = f"fields @timestamp, @message | filter level == \"{severity}\""
    if start_seconds:
        expression += f" | filter @timestamp >= {start_seconds}"
    if end_seconds:
        expression += f" | filter @timestamp <= {end_seconds}"
    client = build_client(SERVICE)
    # Use the /logs API (Insights) to run the query
    response = client.filter_log_events(
        logGroupName=get_log_group(),
        filterPattern=expression,
        startTime=start_seconds or int((datetime.datetime.utcnow() - datetime.timedelta(hours=1)).timestamp()),
        endTime=end_seconds or int(datetime.datetime.utcnow().timestamp()),
        limit=50
    )
    events: List[ErrorEvent] = []
    for ev in response.get("events", []):
        # CloudWatch delivers raw strings; parse JSON if possible
        try:
            payload = json.loads(ev["message"])
        except json.JSONDecodeError:
            payload = {}
        events.append(payload)
    return events