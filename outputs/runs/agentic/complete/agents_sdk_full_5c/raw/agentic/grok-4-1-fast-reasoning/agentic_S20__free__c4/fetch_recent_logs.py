import os
from datetime import datetime, timedelta
from observability_client import query_logs, LogsQueryParams
from typing import Dict, Any

# Datadog provider
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")

def fetch_recent_logs(service: str, field: str, value: str, minutes_back: int = 60) -> Dict[str, Any]:
    """
    Retrieves recent log results filtered by field values and time range from Datadog.
    """
    now = datetime.utcnow()
    from_ts = int((now - timedelta(minutes=minutes_back)).timestamp() * 1000)
    to_ts = int(now.timestamp() * 1000)
    query_str = f"service:{service} {field}:{value}"
    params = LogsQueryParams(
        query=query_str,
        time={"from": from_ts, "to": to_ts}
    )
    return query_logs(params)