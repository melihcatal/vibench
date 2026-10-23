from __future__ import annotations

from typing import Any, Dict

from observability_client import fetch_normalized_entries
from observability_models import LogQueryRequest


def fetch_recent_logs(
    *,
    service: str | None = None,
    field_filters: Dict[str, Any] | None = None,
    correlation_id: str | None = None,
    minutes: int = 15,
    limit: int = 50,
):
    request = LogQueryRequest(
        service=service,
        correlation_id=correlation_id,
        field_filters=field_filters or {},
        minutes=minutes,
        limit=limit,
    )
    return fetch_normalized_entries(request)
