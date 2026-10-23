from datetime import datetime, timedelta
from observability_client import get_logging_client


def fetch_recent_logs(field_filters: dict, hours: int = 1) -> list:
    """Retrieve recent logs from Datadog filtered by field values and time range."""
    client = get_logging_client()
    
    query_parts = [f"{k}:{v}" for k, v in field_filters.items()]
    query = " AND ".join(query_parts)
    
    start_time = (datetime.utcnow() - timedelta(hours=hours)).timestamp()
    end_time = datetime.utcnow().timestamp()
    
    results = client.query_logs(
        query=query,
        time_range=(int(start_time), int(end_time))
    )
    return results.get("logs", [])