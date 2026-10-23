import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from google.cloud import logging_v2
from google.cloud.logging_v2.client import Client as GoogleCloudLoggingClient
from google.cloud.logging_v2.entries import LogEntry
from google.cloud.logging_v2.logger import Logger
from google.cloud.logging_v2.entries import StructEntry


@dataclass
class LogQueryResult:
    entries: List[Dict[str, Any]]


class ManagedLoggingClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.client = GoogleCloudLoggingClient(project=self.project_id)

    def write(self, log_name: str, payload: Dict[str, Any]) -> None:
        logger: Logger = self.client.logger(log_name)
        logger.log_struct(payload)

    def query_error_logs(self, request: Dict[str, Any]) -> LogQueryResult:
        entries = self._read_entries(request)
        return LogQueryResult(entries=entries)

    def fetch_recent_logs(self, request: Dict[str, Any]) -> LogQueryResult:
        entries = self._read_entries(request)
        return LogQueryResult(entries=entries)

    def _read_entries(self, request: Dict[str, Any]) -> List[Dict[str, Any]]:
        filter_parts = []
        log_name = request.get("log_name")
        if log_name:
            filter_parts.append(f'logName="projects/{self.project_id}/logs/{log_name}"')
        severity = request.get("severity")
        if severity:
            filter_parts.append(f'severity>={severity}')
        start_time = request.get("start_time")
        end_time = request.get("end_time")
        if start_time:
            filter_parts.append(f'timestamp>="{start_time.isoformat()}"')
        if end_time:
            filter_parts.append(f'timestamp<="{end_time.isoformat()}"')
        for key, value in (request.get("field_filters") or {}).items():
            filter_parts.append(f'jsonPayload.{key}="{value}"')
        log_filter = " AND ".join(filter_parts) if filter_parts else None
        entries = []
        for entry in self.client.list_entries(filter_=log_filter, order_by=logging_v2.DESCENDING, page_size=50):
            if isinstance(entry, StructEntry):
                entries.append(dict(entry.payload))
            elif isinstance(entry, LogEntry) and isinstance(entry.payload, dict):
                entries.append(dict(entry.payload))
        return entries


class LogsClient:
    def __init__(self, managed_client: ManagedLoggingClient):
        self.managed_client = managed_client

    def query_error_logs(self, request: Dict[str, Any]) -> LogQueryResult:
        return self.managed_client.query_error_logs(request)

    def fetch_recent_logs(self, request: Dict[str, Any]) -> LogQueryResult:
        return self.managed_client.fetch_recent_logs(request)


def resolve_log_name() -> str:
    return os.getenv("GCP_LOG_NAME", "application-log")


def get_logger_client() -> ManagedLoggingClient:
    return ManagedLoggingClient()


def get_logs_client() -> LogsClient:
    return LogsClient(get_logger_client())
