from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional
import uuid

from observability_client import write_log_events
from observability_models import StructuredLogEvent


def write_correlated_logs(
    messages: Iterable[str],
    service: str = "application",
    severity: str = "INFO",
    correlation_id: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    shared_correlation_id = correlation_id or str(uuid.uuid4())
    shared_labels = dict(labels or {})
    shared_labels.setdefault("correlation_id", shared_correlation_id)
    events = [
        StructuredLogEvent(
            message=message,
            severity=severity,
            service=service,
            correlation_id=shared_correlation_id,
            labels=shared_labels,
            extra_fields=dict(extra_fields or {}),
        )
        for message in messages
    ]
    return write_log_events(events)
