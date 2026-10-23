from datetime import datetime, timedelta, timezone

from observability_client import client_from_env
from observability_models import QueryWindow


def query_error_logs(hours: int = 24, severity: str = "ERROR"):
    client = client_from_env()
    end_time = datetime.now(timezone.utc)
    window = QueryWindow(
        start_time=end_time - timedelta(hours=hours), end_time=end_time
    )
    return client.query(severity=severity, window=window)
