from datetime import datetime, timedelta
from observability_client import get_logging_client

def fetch_recent_logs(service: str, field_filters: dict, hours: int = 1):
    client = get_logging_client()
    
    # Construct Datadog Logs API query with field filters
    query_parts = [f"service:{service}"]
    for field, value in field_filters.items():
        query_parts.append(f"{field}:{value}")
    query = " ".join(query_parts)
    
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