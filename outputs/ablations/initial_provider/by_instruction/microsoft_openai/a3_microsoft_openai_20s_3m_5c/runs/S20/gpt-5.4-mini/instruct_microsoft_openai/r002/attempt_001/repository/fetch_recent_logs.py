from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQueryRequest, QueryWindow


def fetch_recent_logs(field_name: str, field_value: str) -> list:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    request = LogQueryRequest(fields={field_name: field_value}, window=QueryWindow(start=start, end=end), limit=100)
    return query_logs(request)
