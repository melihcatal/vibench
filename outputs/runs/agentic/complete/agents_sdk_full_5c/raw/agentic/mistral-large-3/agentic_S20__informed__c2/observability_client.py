"""Local configuration and client helper utilities for Google Cloud Logging."""

import os
from datetime import datetime
from typing import Dict, List, Optional, Union

from google.cloud import logging as google_logging
from google.cloud.logging import Client as GoogleLoggingClient
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging_v2.types import LogEntry as GoogleLogEntry
from google.api_core.exceptions import GoogleAPICallError

from observability_models import LogEntry, QueryFilter, LogQueryResult


class GoogleCloudLoggingClient:
    """Client helper for Google Cloud Logging."""

    def __init__(self, project_id: Optional[str] = None):
        """Initialize the Google Cloud Logging client."""
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
        self.client = GoogleLoggingClient(project=self.project_id)

    def write_log(self, log_entry: LogEntry) -> bool:
        """Write a structured log entry to Google Cloud Logging."""
        try:
            logger = self.client.logger(log_entry.service)
            entry = GoogleLogEntry(
                json_payload=log_entry.to_dict(),
                severity=self._map_severity(log_entry.severity),
                timestamp=log_entry.timestamp,
            )
            logger.log_struct(log_entry.to_dict())
            return True
        except GoogleAPICallError as e:
            print(f"Failed to write log: {e}")
            return False

    def write_correlated_logs(self, log_entries: List[LogEntry]) -> bool:
        """Write multiple correlated log entries to Google Cloud Logging."""
        try:
            for entry in log_entries:
                logger = self.client.logger(entry.service)
                logger.log_struct(entry.to_dict())
            return True
        except GoogleAPICallError as e:
            print(f"Failed to write correlated logs: {e}")
            return False

    def query_logs(self, filter_: QueryFilter, log_name: Optional[str] = None) -> LogQueryResult:
        """Query logs from Google Cloud Logging based on filters."""
        try:
            logger = self.client.logger(log_name) if log_name else None
            filter_str = self._build_filter_string(filter_)

            entries = []
            for entry in self.client.list_entries(
                filter_=filter_str,
                max_results=1000,
                page_size=1000,
            ):
                entries.append(
                    LogEntry(
                        timestamp=entry.timestamp,
                        severity=entry.severity.name,
                        message=entry.payload.get("message", ""),
                        service=entry.logger_name,
                        correlation_id=entry.payload.get("correlation_id"),
                        custom_fields={
                            k: v for k, v in entry.payload.items() 
                            if k not in {"message", "correlation_id"}
                        },
                    )
                )
            return LogQueryResult(entries=entries)
        except GoogleAPICallError as e:
            print(f"Failed to query logs: {e}")
            return LogQueryResult(entries=[])

    def _build_filter_string(self, filter_: QueryFilter) -> str:
        """Build a Google Cloud Logging filter string from QueryFilter."""
        conditions = []
        if filter_.severity:
            conditions.append(f"severity={filter_.severity}")
        if filter_.start_time:
            conditions.append(f"timestamp>=\"{filter_.start_time.isoformat()}\"")
        if filter_.end_time:
            conditions.append(f"timestamp<=\"{filter_.end_time.isoformat()}\"")
        if filter_.correlation_id:
            conditions.append(f"jsonPayload.correlation_id=\"{filter_.correlation_id}\"")
        if filter_.custom_field_filters:
            for key, value in filter_.custom_field_filters.items():
                conditions.append(f"jsonPayload.{key}=\"{value}\"")
        return " AND ".join(conditions)

    def _map_severity(self, severity: str) -> str:
        """Map severity levels to Google Cloud Logging severity."""
        severity_map = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }
        return severity_map.get(severity.upper(), "DEFAULT")