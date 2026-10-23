from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, Optional

from google.cloud import logging as cloud_logging

from observability_models import LogQuery, LogRecord, QueryResult, normalize_fields, parse_log_records

GOOGLE_CLOUD_LOGGING_ENV = "GOOGLE_APPLICATION_CREDENTIALS"
DEFAULT_LOG_NAME = os.getenv("OBSERVABILITY_LOG_NAME", "application")
DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


class ObservabilityClient:
    def __init__(self, project: Optional[str] = None, log_name: str = DEFAULT_LOG_NAME):
        self.project = project or DEFAULT_PROJECT
        self.log_name = log_name
        self._client = cloud_logging.Client(project=self.project)

    def write_log(self, severity: str, message: str, **fields: Any) -> LogRecord:
        timestamp = datetime.now(timezone.utc)
        payload = {
            "severity": severity.upper(),
            "message": message,
            **normalize_fields(fields),
        }
        logger = self._client.logger(self.log_name)
        logger.log_struct(payload, severity=severity.upper(), timestamp=timestamp)
        return LogRecord(timestamp=timestamp, severity=severity.upper(), message=message, fields=normalize_fields(fields))

    def query_logs(self, query: LogQuery) -> QueryResult:
        logger = self._client.logger(self.log_name)
        filter_parts = [f'timestamp >= "{query.start_time.astimezone(timezone.utc).isoformat()}"', f'timestamp <= "{query.end_time.astimezone(timezone.utc).isoformat()}"']
        if query.severity:
            filter_parts.append(f'severity = "{query.severity.upper()}"')
        if query.field_filters:
            for key, value in query.field_filters.items():
                filter_parts.append(f'{key} = "{value}"')
        entries = list(logger.list_entries(filter_=" AND ".join(filter_parts), order_by=cloud_logging.ASCENDING, max_results=query.limit))
        items = []
        for entry in entries:
            payload = dict(entry.payload) if isinstance(entry.payload, Mapping) else {"message": str(entry.payload)}
            payload.setdefault("timestamp", entry.timestamp)
            payload.setdefault("severity", getattr(entry, "severity_text", "INFO"))
            items.append(payload)
        return QueryResult(records=parse_log_records(items), next_token=None)


def get_client() -> ObservabilityClient:
    return ObservabilityClient()
