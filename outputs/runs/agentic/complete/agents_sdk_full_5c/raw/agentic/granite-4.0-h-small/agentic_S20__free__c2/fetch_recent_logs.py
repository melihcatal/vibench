import os
from observability_client import get_logging_client
from datetime import datetime, timedelta

def fetch_recent_logs(filter_by: dict = None, time_range: dict = None) -> list[dict]:
    """Retrieve recent log results filtered by field values and time range.
    Uses a concrete provider (e.g., Elastic Observability Logs API).
    """
    client = get_logging_client()
    query = {}
    if filter_by:
        query["filter"] = filter_by
    if time_range:
        # Assume provider expects ISO8601 timestamps for 'from' and 'to'
        query["time_range"] = time_range
    results = client.fetch_logs(query)
    return results

# Example usage (will be removed in production)
if __name__ == "__main__":
    # Filter by application name and severity, last 10 minutes
    logs = fetch_recent_logs(
        filter_by={"application": "myapp", "level": "info"},
        time_range={"from": (datetime.utcnow() - timedelta(minutes=10)).isoformat() + 'Z',
                    "to": datetime.utcnow().isoformat() + 'Z'}
    )
    print("Fetched logs:", logs)