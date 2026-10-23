from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import QuerySpec, LogResponse, build_correlation_query


def query_error_logs(hours: int = 6, limit: int = 25) -> LogResponse:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    spec = QuerySpec(query='status:error OR status:critical', start=start, end=end, limit=limit)
    data = query_logs(spec)
    return LogResponse(raw=data)
