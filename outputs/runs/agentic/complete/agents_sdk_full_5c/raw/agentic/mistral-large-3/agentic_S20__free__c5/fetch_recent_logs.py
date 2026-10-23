import os
from datetime import datetime, timedelta
from observability_client import get_logging_client

def fetch_recent_logs(field_filters: dict, hours: int = 1) -> list:
    client = get_logging_client()
    start_time = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    query_parts = [f"{k}:{v}" for k, v in field_filters.items()]
    query_parts.append(f"@timestamp:[{start_time} TO {end_time}]")
    query = " AND ".join(query_parts)

    response = client.logs.list_logs(
        project_name=os.getenv("DATADOG_PROJECT", "default"),
        body={
            "query": query,
            "time": {
                "from": start_time,
                "to": end_time
            },
            "limit": 1000
        }
    )
    return response.get("logs", [])