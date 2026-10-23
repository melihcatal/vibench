from __future__ import annotations

from observability_client import DATADOG_API_HOST, query_logs
from observability_models import LogQuery


def query_error_logs(
    service: str,
    from_time: str,
    to_time: str,
    severity: str = "error",
    limit: int = 50,
) -> dict:
    query = LogQuery(
        query=f"service:{service} status:{severity.lower()}",
        from_time=from_time,
        to_time=to_time,
        limit=limit,
    )
    result = query_logs(query)
    return {"provider": "Datadog", "endpoint": DATADOG_API_HOST, **result.to_dict()}
