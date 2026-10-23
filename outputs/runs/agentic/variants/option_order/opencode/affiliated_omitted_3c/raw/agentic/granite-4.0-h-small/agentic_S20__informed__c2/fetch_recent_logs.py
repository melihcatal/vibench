import os
from observability_client import get_log_client


def fetch_recent_logs(field_filter: dict | None = None, minutes_back: int = 30):
    """Retrieve recent log results filtered by field values and time range.

    `field_filter` is a dict of field names to values (e.g., {"level": "INFO"}).
    The function builds a time range relative to now and delegates the query to
    the configured logging client.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes_back)
    client = get_log_client()
    query = {
        "time_range": {
            "start": start_time.isoformat() + "Z",
            "end": end_time.isoformat() + "Z",
        }
    }
    if field_filter:
        query["field_filter"] = field_filter
    # Adapt to the actual SDK/rest method name (e.g., `list_logs`, `search`, etc.)
    logs = client.list_logs(query)
    return logs.get("logs", [])
