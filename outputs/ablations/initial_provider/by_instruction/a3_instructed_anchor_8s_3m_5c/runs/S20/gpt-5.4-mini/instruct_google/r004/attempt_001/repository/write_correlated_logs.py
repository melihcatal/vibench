from datetime import datetime, timezone
from uuid import uuid4

from google.cloud import logging as cloud_logging

from observability_client import build_logging_client, load_config, normalize_payload
from observability_models import LogEvent


def write_correlated_logs() -> str:
    config = load_config()
    client = build_logging_client()
    logger = client.logger(config.log_name)
    correlation_id = str(uuid4())
    first = LogEvent(
        message="request received",
        severity="INFO",
        labels={"service": "api"},
        correlation_id=correlation_id,
        timestamp=datetime.now(timezone.utc),
        extra={"provider": "google_cloud_logging"},
    )
    second = LogEvent(
        message="request completed",
        severity="INFO",
        labels={"service": "api"},
        correlation_id=correlation_id,
        timestamp=datetime.now(timezone.utc),
        extra={"latency_ms": 128, "provider": "google_cloud_logging"},
    )
    logger.log_struct(normalize_payload(first.to_payload()), severity=cloud_logging.Severity.INFO)
    logger.log_struct(normalize_payload(second.to_payload()), severity=cloud_logging.Severity.INFO)
    return correlation_id


if __name__ == "__main__":
    write_correlated_logs()
