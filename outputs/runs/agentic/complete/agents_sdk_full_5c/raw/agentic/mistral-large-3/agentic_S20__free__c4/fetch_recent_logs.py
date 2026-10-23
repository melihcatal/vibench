from datetime import datetime, timedelta
from observability_client import get_log_client

def fetch_recent_logs(field_filters: dict, hours: int = 1) -> list:
    client = get_log_client()
    filter_parts = [
        f"{key}:{value}" for key, value in field_filters.items()
    ]
    filter_str = (
        f"{' AND '.join(filter_parts)} "
        f"timestamp>=\"{datetime.utcnow() - timedelta(hours=hours):%Y-%m-%dT%H:%M:%SZ}\""
    )
    response = client.entries.list(
        body={
            "filter": filter_str,
            "orderBy": "timestamp desc",
            "pageSize": 1000
        }
    )
    return [entry for entry in response.get("entries", [])]