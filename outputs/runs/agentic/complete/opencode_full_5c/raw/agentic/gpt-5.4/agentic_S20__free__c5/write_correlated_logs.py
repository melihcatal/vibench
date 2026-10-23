from __future__ import annotations

from typing import Any

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent, ensure_correlation_id


def write_correlated_logs(
    service: str,
    events: list[dict[str, Any]],
    correlation_id: str | None = None,
) -> dict[str, Any]:
    shared_id = ensure_correlation_id(correlation_id)
    payload = [
        LogEvent(
            service=service,
            level=item.get("level", "INFO"),
            message=item["message"],
            correlation_id=shared_id,
            attributes=dict(item.get("attributes", {})),
        )
        for item in events
    ]
    client = DatadogObservabilityClient()
    result = client.write_logs(payload)
    result["correlation_id"] = shared_id
    return result
