import os
from google.cloud import logging as cloud_logging
from observability_models import CorrelatedLogEntry

client = cloud_logging.Client()
logger = client.logger('correlated-application-logs')


def write_correlated_logs(entries: list[CorrelatedLogEntry]) -> None:
    """Write application log events with a shared correlation identifier to Google Cloud Logging."""
    for entry in entries:
        log_payload = {
            "severity": entry.severity,
            "message": entry.message,
            "timestamp": entry.timestamp.isoformat(),
            "labels": {
                **entry.labels,
                "correlation_id": entry.correlation_id
            },
            "json_payload": entry.custom_fields
        }
        logger.log_struct(log_payload)