from __future__ import annotations

from typing import Any

from observability_client import DATADOG_API_HOST, send_logs
from observability_models import LogEvent


def write_structured_log(
    message: str,
    service: str,
    level: str = "INFO",
    attributes: dict[str, Any] | None = None,
    ddsource: str = "python",
    ddtags: str | None = None,
) -> dict:
    event = LogEvent(
        message=message,
        service=service,
        level=level,
        attributes=attributes or {},
    )
    result = send_logs([event], ddsource=ddsource, ddtags=ddtags)
    return {"provider": "Datadog", "endpoint": DATADOG_API_HOST, "result": result}
