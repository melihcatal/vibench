import os
from google.cloud import logging
from google.cloud.logging_v2 import Client as LoggingClient
from typing import Optional, Dict, Any


class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.client = logging.Client(project=self.project_id)
        self.logger = self.client.logger("application-logs")

    def write_log(
        self,
        message: str,
        severity: str = "INFO",
        labels: Optional[Dict[str, str]] = None,
        trace: Optional[str] = None,
        span_id: Optional[str] = None,
    ) -> None:
        """Write a structured log entry to Google Cloud Logging."""
        entry_payload = {
            "message": message,
            "severity": severity,
            "labels": labels or {},
        }

        if trace:
            entry_payload["trace"] = trace
        if span_id:
            entry_payload["spanId"] = span_id

        self.logger.log_struct(entry_payload, severity=severity)

    def query_logs(
        self, filter_str: str, page_size: int = 100, order_by: str = "timestamp desc"
    ) -> list:
        """Query logs from Google Cloud Logging."""
        entries = self.client.list_entries(
            filter_=filter_str, page_size=page_size, order_by=order_by
        )
        return list(entries)

    def get_client(self) -> LoggingClient:
        """Get the underlying Google Cloud Logging client."""
        return self.client
