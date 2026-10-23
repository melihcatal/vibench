import uuid
from datetime import datetime, timezone

from observability_client import ingest_logs
from observability_models import LogEvent


def write_correlated_logs(
    events: list[dict],
    correlation_id: str | None = None,
) -> dict:
    if not correlation_id:
        correlation_id = str(uuid.uuid4())
    payloads = []
    for evt in events:
        log_event = LogEvent(
            message=evt["message"],
            level=evt.get("level", "info"),
            service=evt.get("service", "unknown"),
            source=evt.get("source", "python"),
            correlation_id=correlation_id,
            timestamp=evt.get("timestamp"),
            extra_attributes=evt.get("extra_attributes", {}),
        )
        payloads.append(log_event.to_dict())
    response = ingest_logs(payloads)
    response.raise_for_status()
    return {
        "status": response.status_code,
        "correlation_id": correlation_id,
        "count": len(payloads),
    }


if __name__ == "__main__":
    request_id = str(uuid.uuid4())
    result = write_correlated_logs(
        events=[
            {
                "message": "Incoming POST /orders request",
                "level": "info",
                "service": "api-gateway",
                "source": "python",
            },
            {
                "message": "Order validation passed",
                "level": "info",
                "service": "order-service",
                "source": "python",
            },
            {
                "message": "Payment processed successfully",
                "level": "info",
                "service": "payment-service",
                "source": "python",
            },
        ],
        correlation_id=request_id,
    )
    print(result)
