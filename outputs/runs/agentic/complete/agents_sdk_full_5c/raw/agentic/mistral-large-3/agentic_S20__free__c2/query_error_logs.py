from datetime import datetime, timedelta
from observability_client import get_logging_client

def query_error_logs(service: str, hours: int = 1, severity: str = "ERROR"):
    client = get_logging_client()
    
    # Datadog Logs API query
    query = f"service:{service} status:{severity}"
    time_range = {
        "from": (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "to": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    response = client.list_logs(
        filter_query=query,
        time_from=time_range["from"],
        time_to=time_range["to"]
    )
    return response