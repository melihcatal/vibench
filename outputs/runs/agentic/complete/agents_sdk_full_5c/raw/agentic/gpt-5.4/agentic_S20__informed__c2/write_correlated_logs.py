from __future__ import annotations

from typing import Iterable, List, Optional

from observability_client import CloudWatchObservabilityClient
from observability_models import LogEvent, ensure_correlation_id



def write_correlated_logs(
    messages: Iterable[str],
    severity: str = "INFO",
    service: str = "application",
    environment: str = "production",
    correlation_id: Optional[str] = None,
) -> dict:
    shared_id = ensure_correlation_id(correlation_id)
    events: List[LogEvent] = [
        LogEvent(
            message=message,
            severity=severity,
            service=service,
            environment=environment,
            correlation_id=shared_id,
        )
        for message in messages
    ]
    client = CloudWatchObservabilityClient()
    return client.put_structured_logs(events)
