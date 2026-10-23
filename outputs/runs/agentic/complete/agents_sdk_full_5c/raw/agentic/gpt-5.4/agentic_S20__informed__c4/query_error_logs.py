from __future__ import annotations

from observability_client import fetch_normalized_entries
from observability_models import LogQueryRequest


def query_error_logs(*, service: str | None = None, minutes: int = 60, limit: int = 100):
    request = LogQueryRequest(service=service, severity="ERROR", minutes=minutes, limit=limit)
    return fetch_normalized_entries(request)
