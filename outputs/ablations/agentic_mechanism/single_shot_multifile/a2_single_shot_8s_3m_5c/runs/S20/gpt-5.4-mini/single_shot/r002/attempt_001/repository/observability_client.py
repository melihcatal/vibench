import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import logging_v2
from google.cloud.logging_v2.entries import LogEntry
from google.cloud.logging_v2.types import WriteLogEntriesRequest

from observability_models import LogQuery, LogResult, ParsedLogResponse


@dataclass
class LogClient:
    project_id: str
    logger_name: str
    client: logging_v2.Client

    def write_log(self, payload: Dict[str, Any]) -> ParsedLogResponse:
        logger = self.client.logger(self.logger_name)
        entry = logger.entry(payload)
        logger.log_struct(entry.payload, severity=payload.get("severity", "DEFAULT"), labels=payload.get("labels"))
        return ParsedLogResponse(status="ok", request_id=payload.get("insert_id", ""), accepted=True, results=[])

    def query_logs(self, query: LogQuery) -> LogResult:
        logger = self.client.logger(self.logger_name)
        filter_parts = []
        if query.severity:
            filter_parts.append(f'severity={query.severity}')
        if query.source:
            filter_parts.append(f'resource.labels.source="{query.source}"')
        if query.field_filters:
            for key, value in query.field_filters.items():
                filter_parts.append(f'jsonPayload.{key}="{value}"')
        filter_parts.append(f'timestamp>="{query.start_time}"')
        filter_parts.append(f'timestamp<="{query.end_time}"')
        entries = list(self.client.list_entries(filter_=" AND ".join(filter_parts), page_size=query.limit))
        results = [
            {
                "timestamp": getattr(entry, "timestamp", None).isoformat() if getattr(entry, "timestamp", None) else None,
                "severity": getattr(entry, "severity", None),
                "payload": dict(getattr(entry, "payload", {}) or {}),
                "insert_id": getattr(entry, "insert_id", None),
            }
            for entry in entries[: query.limit]
        ]
        return LogResult(results=results, count=len(results), query=query)


def get_log_client() -> LogClient:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GCLOUD_PROJECT")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    logger_name = os.getenv("OBSERVABILITY_LOG_NAME", "application-logs")
    return LogClient(project_id=project_id, logger_name=logger_name, client=logging_v2.Client(project=project_id))


def resolve_log_source(default: str) -> str:
    return os.getenv("OBSERVABILITY_LOG_SOURCE", default)
