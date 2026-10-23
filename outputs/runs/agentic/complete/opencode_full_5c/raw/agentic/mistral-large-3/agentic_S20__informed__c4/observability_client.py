import os
from google.cloud import logging as google_logging
from google.cloud.logging_v2.services.logs_ingestion import LogsIngestionClient
from google.oauth2 import service_account


def get_logs_ingestion_client():
    """Initialize and return a Google Cloud Logging client."""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    return google_logging.Client(credentials=credentials)


def get_logs_query_client():
    """Initialize and return a Google Cloud Logging query client."""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    return LogsIngestionClient(credentials=credentials)


def normalize_log_entry(entry: dict) -> dict:
    """Normalize a log entry for Google Cloud Logging."""
    normalized = {
        "severity": entry.get("severity", "INFO").upper(),
        "message": entry.get("message", ""),
        "timestamp": entry.get("timestamp", ""),
        "jsonPayload": entry.get("jsonPayload", {}),
    }
    return normalized
