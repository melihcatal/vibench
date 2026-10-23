from __future__ import annotations

from observability_client import DatadogObservabilityClient
from observability_models import LogQueryRequest


def query_error_logs(
    service: str,
    from_time: str,
    to_time: str,
    severity: str = "error",
    limit: int = 100,
):
    query = f"service:{service} status:{severity.lower()}"
    client = DatadogObservabilityClient()
    request = LogQueryRequest(
        query=query, from_time=from_time, to_time=to_time, limit=limit
    )
    return client.search_logs(request)
