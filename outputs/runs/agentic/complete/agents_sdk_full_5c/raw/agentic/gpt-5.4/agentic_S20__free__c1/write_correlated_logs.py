from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import DatadogObservabilityClient
from observability_models import StructuredLogEvent


def write_correlated_logs(correlation_id: str, service: str, events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    batch: List[StructuredLogEvent] = []
    for item in events:
        payload = dict(item)
        message = payload.pop("message")
        severity = payload.pop("severity", "INFO")
        batch.append(
            StructuredLogEvent(
                message=message,
                service=service,
                severity=severity,
                correlation_id=correlation_id,
                attributes=payload,
            )
        )
    return client.submit_logs(batch)
