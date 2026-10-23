from __future__ import annotations

from typing import Dict, List

from observability_client import DatadogLogsClient
from observability_models import LogQueryRequest, NormalizedLogRecord


def fetch_recent_logs(
    field_filters: Dict[str, str], from_time: str, to_time: str, limit: int = 50
) -> List[NormalizedLogRecord]:
    query = " ".join(f"{key}:{value}" for key, value in field_filters.items())
    request = LogQueryRequest(
        query=query, from_time=from_time, to_time=to_time, limit=limit
    )
    return DatadogLogsClient().search_logs(request)
