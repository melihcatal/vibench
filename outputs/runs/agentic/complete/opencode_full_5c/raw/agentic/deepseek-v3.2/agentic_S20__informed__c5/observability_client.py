import os
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


class ObservabilityClient:
    """Client helper utilities for Google Cloud Logging."""

    def __init__(self, project_id: Optional[str] = None):
        """Initialize Google Cloud Logging client."""
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.client = logging.Client(project=self.project_id)

    def get_logger(self, logger_name: str):
        """Get a logger instance for the specified log name."""
        return self.client.logger(logger_name)

    def write_log(self, logger_name: str, severity: str, message: str, **kwargs):
        """Write a structured log entry."""
        logger = self.get_logger(logger_name)

        log_data = {
            "severity": severity.upper(),
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if kwargs:
            log_data.update(kwargs)

        logger.log_struct(log_data, severity=severity.upper())
        return log_data

    def query_logs(self, filter_str: str, limit: int = 100, order_by: str = DESCENDING):
        """Query logs with a filter string."""
        entries = self.client.list_entries(
            filter_=filter_str, order_by=order_by, page_size=limit
        )

        results = []
        for entry in entries:
            results.append(self._normalize_entry(entry))

        return results

    def query_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        severity: Optional[str] = None,
        service: Optional[str] = None,
        limit: int = 100,
    ):
        """Query logs within a time range with optional filters."""
        filter_str = f'timestamp >= "{start_time.isoformat()}Z"'
        filter_str += f' AND timestamp <= "{end_time.isoformat()}Z"'

        if severity:
            filter_str += f' AND severity = "{severity}"'

        if service:
            filter_str += f' AND jsonPayload.service = "{service}"'

        return self.query_logs(filter_str, limit)

    def _normalize_entry(self, entry) -> Dict[str, Any]:
        """Normalize a log entry to a standard format."""
        normalized = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "resource_type": entry.resource.type if entry.resource else None,
            "resource_labels": entry.resource.labels if entry.resource else {},
            "labels": entry.labels if entry.labels else {},
        }

        if isinstance(entry.payload, dict):
            normalized["payload"] = entry.payload
            normalized["message"] = entry.payload.get("message", "")
        else:
            normalized["payload"] = {"raw": str(entry.payload)}
            normalized["message"] = str(entry.payload)

        return normalized

    @staticmethod
    def build_time_filter(hours_back: int = 24) -> tuple:
        """Build start and end time for a query."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_back)
        return start_time, end_time

    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Get configuration from environment variables."""
        return {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
            "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            "default_logger": os.environ.get("DEFAULT_LOGGER", "application-logs"),
        }
