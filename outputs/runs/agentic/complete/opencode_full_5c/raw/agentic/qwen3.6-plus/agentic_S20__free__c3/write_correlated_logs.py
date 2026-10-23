import os
import json
import uuid
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


def write_correlated_logs(
    messages: list[str],
    correlation_id: Optional[str] = None,
    level: str = "info",
    service: str = "",
    source: str = "",
    hostname: str = "",
    tags: Optional[list[str]] = None,
    attributes_list: Optional[list[dict[str, Any]]] = None,
    api_key: Optional[str] = None,
) -> LogWriteResponse:
    if not correlation_id:
        correlation_id = str(uuid.uuid4())
    events = []
    for idx, msg in enumerate(messages):
        attrs = {}
        if attributes_list and idx < len(attributes_list):
            attrs = attributes_list[idx]
        event = LogEvent(
            message=msg,
            level=level,
            service=service or os.environ.get("DD_SERVICE", ""),
            source=source or "python",
            hostname=hostname or os.environ.get("DD_HOSTNAME", ""),
            tags=(tags or []) + [f"correlation_id:{correlation_id}"],
            correlation_id=correlation_id,
            trace_id=correlation_id,
            timestamp=now_iso(),
            attributes={
                "request.correlation_id": correlation_id,
                "request.sequence": idx,
                **attrs,
            },
        )
        events.append(event)
    return submit_correlated_events(events, correlation_id, api_key=api_key)


def submit_correlated_events(
    events: list[LogEvent],
    correlation_id: str,
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
        "ddtags": f"env:{os.environ.get('DD_ENV', 'production')},correlation_id:{correlation_id}",
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
                message=f"Correlated log events written to Datadog with correlation_id={correlation_id}",
            )
    except urllib.error.HTTPError as e:
        return LogWriteResponse(
            success=False,
            status_code=e.code,
            message=f"Datadog correlated log ingestion failed: {e.reason}",
        )
