import os
import json
import urllib.request
import urllib.error
from typing import Any, Optional

from observability_models import (
    LogEvent,
    LogWriteResponse,
    now_iso,
    DATADOG_LOGS_INTAKE_URL,
    DATADOG_API_KEY,
)


def write_structured_log(
    message: str,
    level: str = "info",
    service: str = "",
    source: str = "",
    hostname: str = "",
    tags: Optional[list[str]] = None,
    attributes: Optional[dict[str, Any]] = None,
    api_key: Optional[str] = None,
) -> LogWriteResponse:
    event = LogEvent(
        message=message,
        level=level,
        service=service or os.environ.get("DD_SERVICE", ""),
        source=source or "python",
        hostname=hostname or os.environ.get("DD_HOSTNAME", ""),
        tags=tags or [],
        timestamp=now_iso(),
        attributes=attributes or {},
    )
    return submit_log_events([event], api_key=api_key)


def submit_log_events(
    events: list[LogEvent],
    api_key: Optional[str] = None,
) -> LogWriteResponse:
    intake_url = f"{DATADOG_LOGS_INTAKE_URL}/api/v2/logs"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key or DATADOG_API_KEY,
    }
    dd_source = os.environ.get("DD_SOURCE", "python")
    if dd_source:
        headers["DD-SOURCE"] = dd_source
    payload = {
        "ddsource": dd_source,
        "ddtags": f"env:{os.environ.get('DD_ENV', 'production')}",
        "hostname": os.environ.get("DD_HOSTNAME", ""),
        "service": os.environ.get("DD_SERVICE", ""),
        "logs": [e.to_dict() for e in events],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(intake_url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return LogWriteResponse(
                success=resp.status in (200, 202, 204),
                status_code=resp.status,
                message="Structured log event written to Datadog Logs Intake API",
            )
    except urllib.error.HTTPError as e:
        return LogWriteResponse(
            success=False,
            status_code=e.code,
            message=f"Datadog log ingestion failed: {e.reason}",
        )
