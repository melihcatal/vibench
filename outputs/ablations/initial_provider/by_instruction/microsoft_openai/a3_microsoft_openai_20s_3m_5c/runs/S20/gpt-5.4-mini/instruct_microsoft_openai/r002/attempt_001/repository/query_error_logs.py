from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQueryRequest, QueryWindow


def query_error_logs() -> list:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=1)
    request = LogQueryRequest(severity="error", window=QueryWindow(start=start, end=end), limit=25)
    return query_logs(request)
