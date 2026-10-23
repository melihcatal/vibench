from __future__ import annotations

from typing import Any, Dict, List

from observability_client import build_query, query_normalized_logs, time_window
from observability_models import LogQueryRequest, join_field_filters


def fetch_recent_logs(
    service: str,
    environment: str,
    field_filters: Dict[str, Any],
    last_minutes: int = 30,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    window = time_window(last_minutes)
    query = build_query(
        f"service:{service}",
        f"env:{environment}",
        join_field_filters(field_filters),
    )
    request = LogQueryRequest(
        query=query, start_time=window["start"], end_time=window["end"], limit=limit
    )
    return query_normalized_logs(request)
