import os
import json
from typing import Optional, Dict, Any, List
from google.cloud import logging
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2._helpers import _datetime_to_rfc3339
from datetime import datetime, timedelta


class ObservabilityClient:
    """Client helper utilities for Google Cloud Logging integration."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get(
            "GOOGLE_CLOUD_PROJECT", "my-project"
        )
        self.client = logging.Client(project=self.project_id)

    def get_logger(self, log_name: str):
        """Get a logger instance for the specified log name."""
        return self.client.logger(log_name)

    def write_log(
        self,
        log_name: str,
        payload: Dict[str, Any],
        severity: str = "INFO",
        labels: Optional[Dict[str, str]] = None,
    ):
        """Write a structured log entry."""
        logger = self.get_logger(log_name)

        if labels is None:
            labels = {}

        logger.log_struct(payload, severity=severity, labels=labels)
        return True

    def query_logs(
        self,
        log_name: str,
        filter_dict: Optional[Dict[str, Any]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        severity: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query logs with flexible filtering."""
        if end_time is None:
            end_time = datetime.utcnow()
        if start_time is None:
            start_time = end_time - timedelta(hours=1)

        filter_parts = [
            f'logName="projects/{self.project_id}/logs/{log_name}"',
            f'timestamp>="{_datetime_to_rfc3339(start_time)}"',
            f'timestamp<="{_datetime_to_rfc3339(end_time)}"',
        ]

        if severity:
            filter_parts.append(f"severity>={severity}")

        if filter_dict:
            for key, value in filter_dict.items():
                if isinstance(value, str):
                    filter_parts.append(f'jsonPayload.{key}="{value}"')
                else:
                    filter_parts.append(f"jsonPayload.{key}={value}")

        filter_str = " AND ".join(filter_parts)

        entries = self.client.list_entries(filter_=filter_str, page_size=limit)

        results = []
        for entry in entries:
            results.append(
                {
                    "timestamp": entry.timestamp,
                    "severity": entry.severity,
                    "payload": entry.payload,
                    "labels": entry.labels,
                    "resource": entry.resource.type if entry.resource else None,
                    "log_name": entry.log_name,
                }
            )

        return results

    def get_error_logs(
        self, log_name: str, hours_back: int = 24, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Convenience method to get error logs."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_back)

        return self.query_logs(
            log_name=log_name,
            start_time=start_time,
            end_time=end_time,
            severity="ERROR",
            limit=limit,
        )

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project"),
            "default_log_name": os.environ.get("DEFAULT_LOG_NAME", "application-logs"),
            "default_region": os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
        }
        return config


def create_correlation_id() -> str:
    """Generate a correlation ID for distributed tracing."""
    import uuid

    return str(uuid.uuid4())


def normalize_log_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize log payload to ensure consistent structure."""
    normalized = payload.copy()

    if "timestamp" not in normalized:
        normalized["timestamp"] = datetime.utcnow().isoformat()

    if "severity" not in normalized:
        normalized["severity"] = "INFO"

    return normalized
