from datetime import datetime, timedelta
from observability_client import get_logging_client


def query_error_logs(severity: str = "ERROR", hours: int = 1) -> list:
    """Query recent error logs from Datadog filtered by severity and time range."""
    client = get_logging_client()
    
    query = f"status:{severity}"
    start_time = (datetime.utcnow() - timedelta(hours=hours)).timestamp()
    end_time = datetime.utcnow().timestamp()
    
    results = client.query_logs(
        query=query,
        time_range=(int(start_time), int(end_time))
    )
    return results.get("logs", [])