from datetime import datetime, timedelta
from observability_client import get_logging_client

def fetch_recent_logs(field_filters: dict, hours: int = 1) -> list:
    """
    Retrieves recent logs from Datadog filtered by field values and time range.
    """
    client = get_logging_client()
    
    query_parts = [f"{key}:{value}" for key, value in field_filters.items()]
    query = " AND ".join(query_parts)
    
    start_time = (datetime.utcnow() - timedelta(hours=hours)).timestamp() * 1000
    end_time = datetime.utcnow().timestamp() * 1000
    
    results = client.query_logs(
        query=query,
        time={
            "from": int(start_time),
            "to": int(end_time)
        }
    )
    
    return results.get("logs", [])