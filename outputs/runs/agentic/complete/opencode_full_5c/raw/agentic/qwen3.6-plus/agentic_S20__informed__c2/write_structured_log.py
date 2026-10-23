import os
import sys
from datetime import datetime, timezone

from observability_models import StructuredLogEvent, SlsClientConfig
from observability_client import ObservabilityClient


def write_structured_log(
    message: str,
    severity: str = "INFO",
    service: str = "default-service",
    source: str = "application",
    attributes: dict | None = None,
) -> dict:
    config = SlsClientConfig.from_env()
    client = ObservabilityClient(config)

    log_event = StructuredLogEvent(
        timestamp=datetime.now(timezone.utc).isoformat(),
        severity=severity,
        message=message,
        service=service,
        source=source,
        attributes=attributes or {},
    )

    result = client.put_logs(
        logs=[log_event],
        topic=service,
        source=source,
    )
    return result


if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Structured log event"
    severity = sys.argv[2] if len(sys.argv) > 2 else "INFO"
    service = (
        sys.argv[3]
        if len(sys.argv) > 3
        else os.environ.get("SERVICE_NAME", "default-service")
    )
    result = write_structured_log(message=message, severity=severity, service=service)
    print(result)
