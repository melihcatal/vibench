import os
from datetime import datetime, timedelta
from observability_client import get_logging_client


def fetch_recent_logs(field_filters: dict, hours: int = 1):
    """Fetch recent logs from Datadog filtered by field values and time range."""
    client = get_logging_client()

    query_parts = [f"{key}:{value}" for key, value in field_filters.items()]
    query_parts.append(f"service:{os.getenv('DD_SERVICE', 'default-service')}")
    query = " ".join(query_parts)

    start_time = int((datetime.utcnow() - timedelta(hours=hours)).timestamp() * 1000)
    end_time = int(datetime.utcnow().timestamp() * 1000)

    results = client.query_logs(
        query=query, time_start=start_time, time_end=end_time, limit=1000
    )

    return results.get("logs", [])
