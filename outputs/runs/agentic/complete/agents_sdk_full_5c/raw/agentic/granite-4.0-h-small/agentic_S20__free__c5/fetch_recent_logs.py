import os
from datetime import datetime, timezone, timedelta
from observability_client import get_log_client

def fetch_recent_logs(event_type: str = None, start_hours: int = 1, field_filter: dict = None) -> list[dict]:
    """Retrieves recent log results filtered by event name and/or field values (Datadog).\n
    Returns a list of log entries (dicts).\n    """
    client = get_log_client()
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=start_hours)
    query_parts = [f"@timestamp:[{int(start.timestamp() * 1000)} TO {int(now.timestamp() * 1000)}]"]
    if event_type:
        query_parts.append(f"event:{event_type}")
    if field_filter:
        for field, value in field_filter.items():
            query_parts.append(f"{field}:{value}")
    query = " AND ".join(query_parts)
    response = client.query_logs(query=query)
    if not response.ok:
        raise RuntimeError(f"Fetch logs query failed: {response.text}")
    return response.json()

if __name__ == "__main__":
    # Example: fetch logs from the last 3 hours where status=\"ERROR\" and service=\"web\"
    logs = fetch_recent_logs(
        event_type="error",
        start_hours=3,
        field_filter={"status": "ERROR", "service": "web"}
    )
    print(json.dumps(logs, indent=2))