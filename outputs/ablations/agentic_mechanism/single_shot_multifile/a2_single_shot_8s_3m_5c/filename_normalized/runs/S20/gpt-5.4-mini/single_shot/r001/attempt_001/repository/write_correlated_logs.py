from datetime import datetime, timezone
import os
import uuid

from observability_client import write_text_entry


if __name__ == "__main__":
    correlation_id = os.getenv("CORRELATION_ID", str(uuid.uuid4()))
    service = os.getenv("SERVICE_NAME", "checkout-api")
    request_id = os.getenv("REQUEST_ID", str(uuid.uuid4()))
    for step, severity in (("received request", "INFO"), ("validated payload", "INFO"), ("completed request", "INFO")):
        write_text_entry(
            f"correlation_id={correlation_id} request_id={request_id} service={service} step={step} ts={datetime.now(timezone.utc).isoformat()}",
            severity=severity,
            labels={"correlation_id": correlation_id, "request_id": request_id, "service": service},
            log_name=os.getenv("OBSERVABILITY_LOG_NAME", "application"),
        )
