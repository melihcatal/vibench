import os
import json
from datetime import datetime
from observability_client import get_logs_ingestion_client


def write_correlated_logs(correlation_id: str, logs: list):
    """Write application log events with a shared correlation identifier to Google Cloud Logging."""
    client = get_logs_ingestion_client()

    entries = []
    for log in logs:
        log_entry = {
            "severity": log.get("level", "INFO").upper(),
            "message": log.get("message", ""),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "jsonPayload": {
                **log.get("custom_fields", {}),
                "correlation_id": correlation_id,
            },
        }
        entries.append(log_entry)

    try:
        client.log_structured(
            log_name="projects/{}/logs/application".format(
                os.getenv("GOOGLE_CLOUD_PROJECT")
            ),
            entries=entries,
            resource={"type": "global"},
        )
    except Exception as e:
        print(f"Failed to write correlated logs to Google Cloud Logging: {e}")
        raise
