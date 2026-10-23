import os
from datetime import datetime, timezone

from observability_client import write_log_record


def main() -> dict:
    record = {
        "timestamp": datetime.now(timezone.utc),
        "severity": os.getenv("LOG_SEVERITY", "INFO"),
        "message": os.getenv("LOG_MESSAGE", "structured event recorded"),
        "service_name": os.getenv("LOG_SERVICE_NAME", "checkout-api"),
        "correlation_id": os.getenv("CORRELATION_ID", "request-001"),
        "event_type": "structured_log",
    }
    result = write_log_record(record)
    return {"status": result.status, "request_id": result.request_id}


if __name__ == "__main__":
    main()
