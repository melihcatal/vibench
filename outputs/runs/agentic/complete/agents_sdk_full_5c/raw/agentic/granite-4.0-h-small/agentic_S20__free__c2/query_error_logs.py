import os
from observability_client import get_logging_client
from datetime import datetime, timedelta

def query_error_logs(severity: str = "error", start_relative: str = "1h") -> list[dict]:
    """Query recent error log entries filtered by severity and time range.
    Uses a concrete provider (e.g., Loki query API).
    """
    client = get_logging_client()
    now = datetime.utcnow()
    # Relative time format supported by the provider; e.g., '1h', '5m', '30s'
    start_time = (now - timedelta(**{token.split('=')[0]: int(token.split('=')[1]) for token in start_relative.split(' ')})).isoformat() + 'Z'
    query = {"query": f"{severity}", "start": start_time, "limit": 100}
    results = client.query_logs(query)
    return results

# Example usage (will be removed in production)
if __name__ == "__main__":
    errors = query_error_logs(severity="error", start_relative="5m")
    print("Found error logs:", errors)