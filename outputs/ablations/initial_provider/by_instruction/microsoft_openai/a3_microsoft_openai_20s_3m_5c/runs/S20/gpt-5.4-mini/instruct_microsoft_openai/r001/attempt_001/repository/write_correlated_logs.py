import os
from datetime import datetime, timezone

from observability_client import write_log_record


def main() -> list[dict]:
    request_id = os.getenv("CORRELATION_ID", "request-001")
    outputs = []
    for step in ("received", "validated", "persisted"):
        result = write_log_record(
            {
                "timestamp": datetime.now(timezone.utc),
                "severity": "INFO",
                "message": f"request {step}",
                "service_name": "checkout-api",
                "correlation_id": request_id,
                "step": step,
            }
        )
        outputs.append({"status": result.status, "request_id": result.request_id})
    return outputs


if __name__ == "__main__":
    main()
