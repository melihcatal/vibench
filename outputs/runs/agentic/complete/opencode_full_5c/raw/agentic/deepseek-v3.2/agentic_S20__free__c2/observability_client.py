import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


class ObservabilityClient:
    """Client helper utilities for Google Cloud Logging integration."""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the Google Cloud Logging client.

        Args:
            project_id: Optional Google Cloud project ID. If not provided,
                       will use the default from environment or credentials.
        """
        self.client = logging.Client(project=project_id)
        self.project_id = self.client.project
        self.default_log_name = os.getenv("DEFAULT_LOG_NAME", "application-logs")

    def get_client_info(self) -> Dict[str, Any]:
        """Get information about the configured logging client."""
        return {
            "project_id": self.project_id,
            "default_log_name": self.default_log_name,
            "client_type": "google.cloud.logging.Client",
            "environment": os.getenv("ENVIRONMENT", "development"),
        }

    def create_logger(self, log_name: Optional[str] = None):
        """
        Create a logger instance for the specified log name.

        Args:
            log_name: Name of the log stream. Uses default if not provided.

        Returns:
            Google Cloud Logging logger instance
        """
        name = log_name or self.default_log_name
        return self.client.logger(name)

    def build_log_entry(
        self,
        severity: str,
        message: str,
        service_name: str,
        structured_data: Optional[Dict] = None,
        labels: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Build a standardized log entry structure.

        Args:
            severity: Log severity level
            message: Human-readable log message
            service_name: Name of the service generating the log
            structured_data: Optional structured fields
            labels: Optional labels for the log entry

        Returns:
            Dictionary with log entry structure
        """
        entry = {
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": service_name,
            "message": message,
            "labels": {
                "environment": os.getenv("ENVIRONMENT", "development"),
                "service_name": service_name,
            },
        }

        if structured_data:
            entry.update(structured_data)

        if labels:
            entry["labels"].update(labels)

        return entry

    def query_logs(
        self,
        filter_str: str,
        hours_back: int = 24,
        limit: int = 100,
        order_by: str = DESCENDING,
    ) -> List[Dict[str, Any]]:
        """
        Execute a log query with standardized parameters.

        Args:
            filter_str: Google Cloud Logging filter string
            hours_back: Number of hours to look back
            limit: Maximum number of entries to return
            order_by: Sort order (DESCENDING or ASCENDING)

        Returns:
            List of log entries
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_back)

        full_filter = f'{filter_str} AND timestamp>="{start_time.isoformat()}Z"'
        full_filter += f' AND timestamp<="{end_time.isoformat()}Z"'

        entries = self.client.list_entries(
            filter_=full_filter, order_by=order_by, page_size=limit
        )

        logs = []
        for entry in entries:
            logs.append(self._normalize_log_entry(entry))
            if len(logs) >= limit:
                break

        return logs

    def _normalize_log_entry(self, entry) -> Dict[str, Any]:
        """Normalize a Google Cloud Logging entry to a standard format."""
        payload = entry.payload if hasattr(entry, "payload") else {}

        normalized = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "log_name": entry.log_name.split("/")[-1] if entry.log_name else None,
            "message": payload.get("message", ""),
            "payload": dict(payload),
            "labels": dict(entry.labels) if entry.labels else {},
            "resource": {
                "type": entry.resource.type if entry.resource else None,
                "labels": dict(entry.resource.labels)
                if entry.resource and entry.resource.labels
                else {},
            },
            "insert_id": entry.insert_id,
        }

        return normalized

    def get_service_logs(
        self,
        service_name: str,
        hours_back: int = 1,
        severity: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get logs for a specific service.

        Args:
            service_name: Name of the service
            hours_back: Number of hours to look back
            severity: Optional severity filter
            limit: Maximum number of entries

        Returns:
            List of log entries for the service
        """
        filter_str = f'jsonPayload.service="{service_name}"'
        if severity:
            filter_str += f" AND severity>={severity}"

        return self.query_logs(filter_str, hours_back, limit)

    def get_correlated_logs(
        self, correlation_id: str, hours_back: int = 24, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all logs with a specific correlation ID.

        Args:
            correlation_id: Correlation identifier
            hours_back: Number of hours to look back
            limit: Maximum number of entries

        Returns:
            List of correlated log entries
        """
        filter_str = f'jsonPayload.correlation_id="{correlation_id}"'
        return self.query_logs(filter_str, hours_back, limit)


# Singleton instance for easy import
client = ObservabilityClient()
