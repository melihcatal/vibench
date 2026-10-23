import os
from datetime import datetime, timedelta
from observability_client import get_logging_client


def query_error_logs(severity: str = "ERROR", hours: int = 1):
    """Query recent error logs from Datadog filtered by severity and time range."""
    client = get_logging_client()

    query = f"status:{severity} service:{os.getenv('DD_SERVICE', 'default-service')}"
    start_time = int((datetime.utcnow() - timedelta(hours=hours)).timestamp() * 1000)
    end_time = int(datetime.utcnow().timestamp() * 1000)

    results = client.query_logs(
        query=query, time_start=start_time, time_end=end_time, limit=1000
    )

    return results.get("logs", [])
