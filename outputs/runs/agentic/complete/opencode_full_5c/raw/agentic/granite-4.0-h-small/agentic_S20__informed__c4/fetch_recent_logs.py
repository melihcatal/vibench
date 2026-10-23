import datetime
from observability_client import get_log_client


def fetch_recent_logs(duration_minutes: int = 60, field_filter: dict | None = None):
    """Retrieve recent log results filtered by field values and time range.

    Uses the configured provider client to request logs from the last `duration_minutes`.
    Optional `field_filter` can narrow results by specific field values.
    """
    client = get_log_client()
    start_time = datetime.utcnow() - datetime.timedelta(minutes=duration_minutes)
    query = {
        "startTime": start_time.isoformat() + "Z",
        "endTime": datetime.utcnow().isoformat() + "Z",
    }
    if field_filter:
        query["filter"] = field_filter
    try:
        logs = client.fetch_logs(query)
        return logs
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []
