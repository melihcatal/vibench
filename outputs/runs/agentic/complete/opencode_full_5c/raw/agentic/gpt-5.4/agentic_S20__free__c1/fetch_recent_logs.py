from __future__ import annotations

from observability_client import DATADOG_API_HOST, query_logs
from observability_models import LogQuery


def fetch_recent_logs(
    service: str,
    field_filters: dict[str, str],
    from_time: str,
    to_time: str,
    limit: int = 50,
) -> dict:
    query_parts = [f"service:{service}"] + [
        f"{key}:{value}" for key, value in field_filters.items()
    ]
    query = LogQuery(
        query=" ".join(query_parts),
        from_time=from_time,
        to_time=to_time,
        limit=limit,
    )
    result = query_logs(query)
    return {"provider": "Datadog", "endpoint": DATADOG_API_HOST, **result.to_dict()}
