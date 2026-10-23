import datetime
from observability_client import get_client

def fetch_recent_logs(start_time: str = None, end_time: str = None, field_filter: dict = None, limit: int = 50):
    """Retrieve recent log results filtered by field values and time range.

    Args:
        start_time: ISO8601 timestamp to start the query.
        end_time: ISO8601 timestamp to end the query.
        field_filter: Dict of field names to values to match exactly.
        limit: Maximum number of log entries to return.
    Returns:
        List of matching log entries (dict).
    """
    client = get_client()
    query = {
        "filter": {
            "timestamp_from": start_time or client.now_iso()[:-7] + "Z",
            "timestamp_to": end_time or client.now_iso()[:-7] + "Z",
        },
    }
    if field_filter:
        query["filter"].update(field_filter)
    query["limit"] = limit
    response = client.post("/v1/logs/query", json=query)
    response.raise_for_status()
    return response.json().get("logs", [])
