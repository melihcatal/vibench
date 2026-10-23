from __future__ import annotations

from typing import Any

from observability_client import DATADOG_API_HOST, send_logs
from observability_models import LogEvent


def write_correlated_logs(
    correlation_id: str,
    service: str,
    events: list[dict[str, Any]],
    ddsource: str = "python",
    ddtags: str | None = None,
) -> dict:
    payload = [
        LogEvent(
            message=str(item["message"]),
            service=service,
            level=str(item.get("level", "INFO")),
            timestamp=str(item.get("timestamp") or None)
            if item.get("timestamp")
            else None,
            correlation_id=correlation_id,
            attributes={
                k: v
                for k, v in item.items()
                if k not in {"message", "level", "timestamp"}
            },
        )
        for item in events
    ]
    result = send_logs(payload, ddsource=ddsource, ddtags=ddtags)
    return {
        "provider": "Datadog",
        "endpoint": DATADOG_API_HOST,
        "correlation_id": correlation_id,
        "result": result,
    }
