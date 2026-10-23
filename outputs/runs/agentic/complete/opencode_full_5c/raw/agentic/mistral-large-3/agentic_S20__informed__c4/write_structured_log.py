import json
import os
from datetime import datetime
from observability_client import get_logs_ingestion_client


def write_structured_log(level: str, message: str, **custom_fields):
    """Write a structured JSON log event to Google Cloud Logging."""
    client = get_logs_ingestion_client()

    log_entry = {
        "severity": level.upper(),
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "jsonPayload": custom_fields,
    }

    try:
        client.log_structured(
            log_name="projects/{}/logs/application".format(
                os.getenv("GOOGLE_CLOUD_PROJECT")
            ),
            entries=[log_entry],
            resource={"type": "global"},
        )
    except Exception as e:
        print(f"Failed to write log to Google Cloud Logging: {e}")
        raise
