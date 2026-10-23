from datetime import datetime, timedelta
from observability_client import get_logging_client

def query_error_logs(severity: str = "ERROR", hours: int = 1) -> list:
    """
    Queries recent error log entries from Datadog filtered by severity and time range.
    """
    client = get_logging_client()
    
    query = f"status:{severity}"
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