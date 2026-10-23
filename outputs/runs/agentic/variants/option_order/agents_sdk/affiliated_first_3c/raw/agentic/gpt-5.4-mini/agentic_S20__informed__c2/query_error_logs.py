from datetime import datetime, timedelta, timezone

from observability_client import query_logs

DATADOG_ERROR_QUERY = 'status:error OR status:critical'


def query_error_logs(minutes: int = 60, limit: int = 25):
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    query = f"({DATADOG_ERROR_QUERY})"
    return query_logs(query=query, start=start, end=end, limit=limit)
