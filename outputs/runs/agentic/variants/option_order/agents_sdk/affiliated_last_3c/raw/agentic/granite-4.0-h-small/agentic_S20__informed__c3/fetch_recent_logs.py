import os
import json
from observability_client import get_cloudwatch_logs_client
from observability_models import LogQueryParams

def fetch_recent_logs(time_range_minutes: int = 15, field_filter: dict = None):
    """Retrieve recent logs filtered by field values and time range from CloudWatch Logs.
    Args:
        time_range_minutes: How far back to look relative to now.
        field_filter: Optional dict of key/value pairs to match on extracted fields.
    Returns:
        List of log event dicts that satisfy the filter.
    """
    client = get_cloudwatch_logs_client()
    log_group = "/aws/myapp/structured-logs"
    now_sec = int(time.time())
    start_sec = now_sec - time_range_minutes * 60

    # Pull raw events
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=int(start_sec * 1000),
        endTime=int(now_sec * 1000)
    )
    events = response.get("events", [])

    # Simple in‑memory field extraction and filtering
    field_names = ["level", "service", "correlationId"]
    extracted = []
    for ev in events:
        try:
            msg = json.loads(ev["message"])
        except Exception:
            continue
        fields = {k: v for k, v in msg.items() if k in field_names}
        if field_filter:
            if all(fields.get(k) == v for k, v in field_filter.items()):
                extracted.append(ev)
        else:
            extracted.append(ev)
    return extracted
