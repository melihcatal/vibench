from datetime import datetime, timedelta
from observability_client import get_log_client

def query_error_logs(severity: str = "ERROR", hours: int = 1) -> list:
    client = get_log_client()
    filter_str = (
        f"severity={severity} "
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