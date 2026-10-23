from __future__ import annotations

from typing import Any, Dict

from observability_client import send_logs
from observability_models import LogEvent


def write_structured_log(
    service: str,
    environment: str,
    level: str,
    message: str,
    attributes: Dict[str, Any],
) -> Dict[str, Any]:
    event = LogEvent(
        service=service,
        environment=environment,
        level=level,
        message=message,
        attributes=attributes,
    )
    return send_logs([event])
