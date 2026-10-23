import os
from datetime import datetime, timezone, timedelta
from observability_client import get_log_client

def query_error_logs(severity: str = "ERROR", start_hours: int = 24) -> list[dict]:
    """Queries recent error logs filtered by severity and time range (Datadog).\n
    Returns a list of log dictionaries.\n    """
    client = get_log_client()
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=start_hours)
    response = client.query_logs(
        query=f"status:error severity:{severity}",
        from_timestamp=int(start.timestamp() * 1000),  # Datadog expects ms
        to_timestamp=int(now.timestamp() * 1000)
    )
    if not response.ok:
        raise RuntimeError(f"Log query failed: {response.text}")
    return response.json()

if __name__ == "__main__":
    # Example usage: fetch all ERROR logs from the last 48 hours
    errors = query_error_logs(severity="ERROR", start_hours=48)
    print(json.dumps(errors, indent=2))