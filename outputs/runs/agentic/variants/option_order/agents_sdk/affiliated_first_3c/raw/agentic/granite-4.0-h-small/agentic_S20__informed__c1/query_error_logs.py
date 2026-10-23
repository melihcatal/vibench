import datetime
from observability_client import get_client

def query_error_logs(start_time: str = None, end_time: str = None, limit: int = 20):
    """Query recent error log entries filtered by severity and time range.

    Args:
        start_time: ISO8601 timestamp to start the query.
        end_time: ISO8601 timestamp to end the query.
        limit: Maximum number of log entries to return.
    Returns:
        List of log entries (dict) that are errors.
    """
    client = get_client()
    query = {
        "filter": {
            "level": "error",
        },
    }
    if start_time:
        query["filter"]["timestamp_from"] = start_time
    if end_time:
        query["filter"]["timestamp_to"] = end_time
    query["limit"] = limit
    response = client.post("/v1/logs/query", json=query)
    response.raise_for_status()
    return response.json().get("logs", [])
