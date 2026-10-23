from datetime import datetime, timezone

from google.cloud import logging as cloud_logging

from observability_client import build_logging_client, load_config, normalize_payload
from observability_models import LogEvent


def write_structured_log() -> str:
    config = load_config()
    client = build_logging_client()
    logger = client.logger(config.log_name)
    event = LogEvent(
        message="structured event written",
        severity="INFO",
        labels={"service": "checkout", "env": "prod"},
        timestamp=datetime.now(timezone.utc),
        extra={"operation": "write_structured_log", "provider": "google_cloud_logging"},
    )
    payload = normalize_payload(event.to_payload())
    logger.log_struct(payload, severity=cloud_logging.Severity.INFO)
    return "logged"


if __name__ == "__main__":
    write_structured_log()
