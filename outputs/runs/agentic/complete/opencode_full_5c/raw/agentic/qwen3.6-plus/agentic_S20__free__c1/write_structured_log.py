import os
import json
import requests
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from observability_client import (
    DATADOG_LOG_INTAKE_ENDPOINT,
    get_datadog_log_intake_headers,
    build_datadog_log_payload,
)
from observability_models import LogEvent, serialize_log_event


def write_structured_log(
    message: str,
    level: str = "info",
    service: Optional[str] = None,
    hostname: Optional[str] = None,
    ddsource: Optional[str] = None,
    ddtags: Optional[str] = None,
    custom_attributes: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    event = LogEvent(
        message=message,
        level=level,
        service=service,
        hostname=hostname,
        ddsource=ddsource,
        ddtags=ddtags,
        custom_attributes=custom_attributes or {},
        timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
    )

    payload = event.to_datadog_payload()
    headers = get_datadog_log_intake_headers()

    response = requests.post(
        DATADOG_LOG_INTAKE_ENDPOINT,
        headers=headers,
        data=json.dumps([payload]),
        timeout=30,
    )

    if response.status_code not in (200, 202, 204):
        raise RuntimeError(
            f"Datadog log ingestion failed with status {response.status_code}: {response.text}"
        )

    return {
        "status": "success",
        "event_id": event.timestamp,
        "datadog_status": response.status_code,
        "message": message,
        "level": level,
    }


if __name__ == "__main__":
    result = write_structured_log(
        message="Application startup complete",
        level="info",
        service=os.getenv("DATADOG_SERVICE", "default-service"),
        custom_attributes={
            "version": "2.1.0",
            "environment": os.getenv("APP_ENV", "production"),
        },
    )
    print(json.dumps(result, indent=2))
