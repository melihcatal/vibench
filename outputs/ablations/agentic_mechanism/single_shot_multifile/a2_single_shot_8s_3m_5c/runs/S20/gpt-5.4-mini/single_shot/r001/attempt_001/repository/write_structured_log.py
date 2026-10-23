from datetime import datetime, timezone
import os
import uuid

from observability_client import write_structured_entry


if __name__ == "__main__":
    event = {
        "event_type": "structured_log_write",
        "service": os.getenv("SERVICE_NAME", "checkout-api"),
        "severity": "INFO",
        "message": "structured log event written",
        "timestamp": datetime.now(timezone.utc),
        "insert_id": str(uuid.uuid4()),
        "environment": os.getenv("ENVIRONMENT", "production"),
    }
    write_structured_entry(event, severity="INFO", log_name=os.getenv("OBSERVABILITY_LOG_NAME", "application"))
