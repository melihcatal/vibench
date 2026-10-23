import os
import json
import uuid
import requests
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from observability_client import (
    DATADOG_LOG_INTAKE_ENDPOINT,
    get_datadog_log_intake_headers,
)
from observability_models import LogEvent


def write_correlated_logs(
    messages: List[Dict[str, str]],
    correlation_id: Optional[str] = None,
    service: Optional[str] = None,
    hostname: Optional[str] = None,
    ddsource: Optional[str] = None,
    ddtags: Optional[str] = None,
) -> Dict[str, Any]:
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    events = []
    for msg_data in messages:
        event = LogEvent(
            message=msg_data["message"],
            level=msg_data.get("level", "info"),
            service=service or os.getenv("DATADOG_SERVICE", "default-service"),
            hostname=hostname,
            ddsource=ddsource,
            ddtags=ddtags,
            correlation_id=correlation_id,
            custom_attributes=msg_data.get("attributes", {}),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        events.append(event.to_datadog_payload())

    headers = get_datadog_log_intake_headers()

    response = requests.post(
        DATADOG_LOG_INTAKE_ENDPOINT,
        headers=headers,
        data=json.dumps(events),
        timeout=30,
    )

    if response.status_code not in (200, 202, 204):
        raise RuntimeError(
            f"Datadog correlated log ingestion failed with status {response.status_code}: {response.text}"
        )

    return {
        "status": "success",
        "correlation_id": correlation_id,
        "events_written": len(events),
        "datadog_status": response.status_code,
    }


def write_request_trace_logs(
    request_id: str,
    trace_steps: List[Dict[str, str]],
    service: Optional[str] = None,
    hostname: Optional[str] = None,
) -> Dict[str, Any]:
    messages = []
    for step in trace_steps:
        messages.append(
            {
                "message": step["message"],
                "level": step.get("level", "info"),
                "attributes": {
                    "request_id": request_id,
                    "step": step.get("step", ""),
                    "duration_ms": step.get("duration_ms", 0),
                },
            }
        )

    return write_correlated_logs(
        messages=messages,
        correlation_id=request_id,
        service=service,
        hostname=hostname,
        ddtags=f"request_id:{request_id}",
    )


if __name__ == "__main__":
    req_id = str(uuid.uuid4())
    result = write_request_trace_logs(
        request_id=req_id,
        trace_steps=[
            {
                "message": "Request received",
                "level": "info",
                "step": "ingest",
                "duration_ms": 5,
            },
            {
                "message": "Validation passed",
                "level": "info",
                "step": "validate",
                "duration_ms": 12,
            },
            {
                "message": "Processing complete",
                "level": "info",
                "step": "process",
                "duration_ms": 150,
            },
        ],
    )
    print(json.dumps(result, indent=2))
