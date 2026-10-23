from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent, ensure_correlation_id


def write_correlated_logs(
    service: str,
    messages: Iterable[str],
    severity: str = "INFO",
    correlation_id: Optional[str] = None,
    common_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    shared_id = ensure_correlation_id(correlation_id)
    attrs = common_attributes or {}
    logs: List[Dict[str, Any]] = []
    for index, message in enumerate(messages):
        event = LogEvent(
            message=message,
            service=service,
            severity=severity,
            correlation_id=shared_id,
            attributes={**attrs, "event_index": index},
        )
        logs.append(
            event.to_datadog_log(
                ddsource="python",
                ddtags=[f"service:{service}", f"correlation_id:{shared_id}"],
            )
        )
    client = DatadogObservabilityClient()
    response = client.submit_logs(logs)
    response["correlation_id"] = shared_id
    return response
