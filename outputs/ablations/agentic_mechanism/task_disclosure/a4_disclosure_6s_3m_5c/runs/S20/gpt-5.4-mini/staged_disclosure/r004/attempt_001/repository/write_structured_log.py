import json
import os
from datetime import datetime, timezone

from google.cloud import logging as cloud_logging


def write_structured_log() -> None:
    client = cloud_logging.Client()
    logger = client.logger("structured-json-log")
    payload = {
        "event": "structured_log_write",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "google_cloud_logging",
        "severity": "INFO",
        "details": {
            "message": os.getenv("LOG_MESSAGE", "structured log event"),
            "request_id": os.getenv("REQUEST_ID", "unknown"),
        },
    }
    logger.log_struct(payload, severity="INFO")


if __name__ == "__main__":
    write_structured_log()
