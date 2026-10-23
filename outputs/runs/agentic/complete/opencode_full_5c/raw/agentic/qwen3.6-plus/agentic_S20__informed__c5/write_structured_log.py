import os
import json
import sys
from typing import Any

from observability_models import LogEvent, LogSeverity, IngestionResponse
from observability_client import ingest_log_events


def write_structured_log(
    message: str,
    severity: str = LogSeverity.INFO,
    service: str = "",
    source: str = "",
    hostname: str = "",
    attributes: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> IngestionResponse:
    event = LogEvent.now(
        message=message,
        severity=severity,
        service=service or os.environ.get("DD_SERVICE", "default-service"),
        source=source or os.environ.get("DD_SOURCE", "python-app"),
        hostname=hostname or os.environ.get("DD_HOSTNAME", ""),
        attributes=attributes or {},
        tags=tags or [],
    )
    result = ingest_log_events([event])
    return result


def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "Structured log event"
    severity = sys.argv[2] if len(sys.argv) > 2 else LogSeverity.INFO
    service = sys.argv[3] if len(sys.argv) > 3 else ""

    result = write_structured_log(
        message=message,
        severity=severity,
        service=service,
        attributes={"environment": os.environ.get("DD_ENV", "production")},
    )
    print(
        json.dumps(
            {
                "success": result.success,
                "status_code": result.status_code,
                "event_ids": result.event_ids,
            }
        )
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
