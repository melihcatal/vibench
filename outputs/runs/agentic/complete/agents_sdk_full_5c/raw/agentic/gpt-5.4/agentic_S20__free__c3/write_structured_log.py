from __future__ import annotations

from typing import Any, Dict

from observability_client import submit_log_events
from observability_models import LogEvent


DATADOG_PROVIDER = "Datadog"


def write_structured_log(
    service: str,
    level: str,
    message: str,
    environment: str,
    extra_fields: Dict[str, Any] | None = None,
):
    event = LogEvent(
        service=service,
        level=level,
        message=message,
        environment=environment,
        fields=extra_fields or {},
    )
    return submit_log_events([event])
