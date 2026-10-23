import os
import sys
import uuid
from datetime import datetime, timezone

from observability_models import StructuredLogEvent, SlsClientConfig
from observability_client import ObservabilityClient


def write_correlated_logs(
    correlation_id: str | None = None,
    request_id: str | None = None,
    service: str = "default-service",
    source: str = "application",
    log_entries: list[dict] | None = None,
) -> dict:
    config = SlsClientConfig.from_env()
    client = ObservabilityClient(config)

    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    if request_id is None:
        request_id = str(uuid.uuid4())

    if log_entries is None:
        log_entries = [
            {"severity": "INFO", "message": f"Request {request_id} started"},
            {"severity": "INFO", "message": f"Processing request {request_id}"},
            {"severity": "INFO", "message": f"Request {request_id} completed"},
        ]

    log_events = []
    for entry in log_entries:
        log_event = StructuredLogEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            severity=entry.get("severity", "INFO"),
            message=entry.get("message", ""),
            service=service,
            correlation_id=correlation_id,
            request_id=request_id,
            source=source,
            attributes=entry.get("attributes", {}),
        )
        log_events.append(log_event)

    result = client.put_logs(
        logs=log_events,
        topic=f"{service}-correlated",
        source=source,
    )
    return {
        "correlation_id": correlation_id,
        "request_id": request_id,
        "log_count": len(log_events),
        "write_result": result,
    }


if __name__ == "__main__":
    correlation_id = sys.argv[1] if len(sys.argv) > 1 else None
    service = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.environ.get("SERVICE_NAME", "default-service")
    )
    result = write_correlated_logs(correlation_id=correlation_id, service=service)
    print(result)
