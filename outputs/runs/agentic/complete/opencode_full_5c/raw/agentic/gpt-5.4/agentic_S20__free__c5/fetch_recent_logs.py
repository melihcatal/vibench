from __future__ import annotations

from observability_client import DatadogObservabilityClient
from observability_models import LogQueryRequest


def fetch_recent_logs(
    service: str,
    from_time: str,
    to_time: str,
    field_filters: dict[str, str] | None = None,
    limit: int = 50,
):
    filters = [f"service:{service}"]
    for key, value in sorted((field_filters or {}).items()):
        filters.append(f"@{key}:{value}")
    request = LogQueryRequest(
        query=" ".join(filters),
        from_time=from_time,
        to_time=to_time,
        limit=limit,
    )
    client = DatadogObservabilityClient()
    return client.search_logs(request)
