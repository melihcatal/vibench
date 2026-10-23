import os
from datetime import datetime, timedelta
from observability_client import query_logs, LogsQueryParams
from typing import Dict, Any

# Datadog provider
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")

def query_error_logs(service: str = "myapp", minutes_back: int = 60) -> Dict[str, Any]:
    """
    Queries recent error log entries filtered by severity and time range from Datadog.
    """
    now = datetime.utcnow()
    from_ts = int((now - timedelta(minutes=minutes_back)).timestamp() * 1000)
    to_ts = int(now.timestamp() * 1000)
    params = LogsQueryParams(
        query=f"service:{service} @severity:ERROR",
        time={"from": from_ts, "to": to_ts}
    )
    return query_logs(params)