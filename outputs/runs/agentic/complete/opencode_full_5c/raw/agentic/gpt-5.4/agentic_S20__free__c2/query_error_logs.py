from __future__ import annotations

from typing import Any, Dict, List

from observability_client import build_query, query_normalized_logs, time_window
from observability_models import LogQueryRequest


def query_error_logs(
    service: str,
    environment: str,
    last_minutes: int = 60,
    severity: str = "error",
    limit: int = 100,
) -> List[Dict[str, Any]]:
    window = time_window(last_minutes)
    query = build_query(
        f"service:{service}", f"env:{environment}", f"status:{severity}"
    )
    request = LogQueryRequest(
        query=query, start_time=window["start"], end_time=window["end"], limit=limit
    )
    return query_normalized_logs(request)
