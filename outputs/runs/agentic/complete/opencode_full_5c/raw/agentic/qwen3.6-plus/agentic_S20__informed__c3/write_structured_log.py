import os
from datetime import datetime, timezone

from observability_client import ingest_logs, build_log_payload
from observability_models import LogEvent


def write_structured_log(
    message: str,
    level: str,
    service: str,
    source: str,
    extra_attributes: dict | None = None,
    timestamp: datetime | None = None,
) -> dict:
    event = LogEvent(
        message=message,
        level=level,
        service=service,
        source=source,
        extra_attributes=extra_attributes or {},
        timestamp=timestamp,
    )
    payload = event.to_dict()
    response = ingest_logs([payload])
    response.raise_for_status()
    return {
        "status": response.status_code,
        "message": "log ingested",
        "timestamp": payload["timestamp"],
    }


if __name__ == "__main__":
    result = write_structured_log(
        message="Application started successfully",
        level="info",
        service="web-api",
        source="python",
        extra_attributes={
            "version": "1.2.0",
            "environment": os.environ.get("ENV", "production"),
        },
    )
    print(result)
