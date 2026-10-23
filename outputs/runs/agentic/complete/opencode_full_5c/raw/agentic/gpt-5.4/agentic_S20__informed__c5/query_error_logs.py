from __future__ import annotations

from typing import List

from observability_client import DatadogLogsClient
from observability_models import LogQueryRequest, NormalizedLogRecord


def query_error_logs(
    service: str,
    from_time: str,
    to_time: str,
    severity: str = "error",
    limit: int = 100,
) -> List[NormalizedLogRecord]:
    query = f"service:{service} status:{severity}"
    request = LogQueryRequest(
        query=query, from_time=from_time, to_time=to_time, limit=limit
    )
    return DatadogLogsClient().search_logs(request)
