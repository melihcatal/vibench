import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2.resource import Resource


class ObservabilityClient:
    """Client helper utilities for Google Cloud Logging integration."""

    def __init__(self, project_id: Optional[str] = None):
        """Initialize Google Cloud Logging client."""
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.client = logging.Client(project=self.project_id)

    def get_logger(self, log_name: str):
        """Get a logger instance for a specific log name."""
        return self.client.logger(log_name)

    def write_log(
        self,
        log_name: str,
        payload: Dict[str, Any],
        severity: str = "INFO",
        labels: Optional[Dict[str, str]] = None,
        resource_type: str = "global",
        resource_labels: Optional[Dict[str, str]] = None,
    ):
        """Write a structured log entry."""
        logger = self.get_logger(log_name)

        # Create resource
        resource = Resource(type=resource_type, labels=resource_labels or {})

        # Write log entry
        logger.log_struct(
            payload, severity=severity, resource=resource, labels=labels or {}
        )

        return {"log_name": log_name, "severity": severity, "payload": payload}

    def query_logs(
        self, filter_query: str, order_by: str = "timestamp desc", page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Query logs using Cloud Logging filter syntax."""
        entries = self.client.list_entries(
            filter_=filter_query, order_by=order_by, page_size=page_size
        )

        results = []
        for entry in entries:
            entry_data = self._normalize_log_entry(entry)
            results.append(entry_data)

            if len(results) >= page_size:
                break

        return results

    def query_recent_logs(
        self,
        time_minutes: int = 30,
        severity: Optional[str] = None,
        service_name: Optional[str] = None,
        log_name_filter: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Query recent logs with common filters."""
        # Calculate time range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=time_minutes)

        # Build query
        query_parts = [
            f'timestamp>="{start_time.isoformat()}Z"',
            f'timestamp<="{end_time.isoformat()}Z"',
        ]

        if severity:
            query_parts.append(f'severity="{severity}"')

        if service_name:
            query_parts.append(f'resource.labels.service="{service_name}"')

        if log_name_filter:
            query_parts.append(f'logName="{log_name_filter}"')

        query = " AND ".join(query_parts)

        entries = self.query_logs(query, page_size=limit)

        # Calculate statistics
        severity_counts = {}
        for entry in entries:
            sev = entry.get("severity", "DEFAULT")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        return {
            "query": query,
            "time_range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "minutes": time_minutes,
            },
            "total_results": len(entries),
            "severity_distribution": severity_counts,
            "results": entries,
        }

    def _normalize_log_entry(self, entry) -> Dict[str, Any]:
        """Normalize a Cloud Logging entry to a standard dictionary format."""
        entry_data = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "log_name": entry.log_name,
            "resource_type": entry.resource.type,
            "resource_labels": dict(entry.resource.labels)
            if entry.resource.labels
            else {},
            "labels": dict(entry.labels) if entry.labels else {},
            "trace": entry.trace if hasattr(entry, "trace") else None,
            "span_id": entry.span_id if hasattr(entry, "span_id") else None,
        }

        # Extract payload
        if isinstance(entry.payload, dict):
            entry_data["payload"] = entry.payload
            entry_data["message"] = entry.payload.get("message", str(entry.payload))
        else:
            entry_data["payload"] = str(entry.payload)
            entry_data["message"] = str(entry.payload)

        return entry_data

    @staticmethod
    def build_correlation_payload(
        base_payload: Dict[str, Any],
        correlation_id: str,
        sequence: Optional[int] = None,
        total_sequences: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Build a payload with correlation metadata."""
        payload = base_payload.copy()
        payload["correlation_id"] = correlation_id

        if sequence is not None:
            payload["sequence"] = sequence

        if total_sequences is not None:
            payload["total_sequences"] = total_sequences

        return payload

    @staticmethod
    def get_environment_config() -> Dict[str, str]:
        """Get observability configuration from environment variables."""
        return {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
            "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            "default_log_name": os.environ.get("DEFAULT_LOG_NAME", "application-logs"),
            "default_service_name": os.environ.get("SERVICE_NAME", "unknown-service"),
        }
