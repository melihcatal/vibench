from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from google.cloud import logging as gcloud_logging
from google.cloud import logging_v2

from observability_models import LogQuery, LogRecord, QueryResult, normalize_log_name


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    logger_name: str = "application"

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        if not project_id:
            raise RuntimeError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required for Google Cloud Logging")
        return cls(project_id=project_id, logger_name=os.getenv("LOG_NAME", "application"))


class ObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None) -> None:
        self.config = config or ObservabilityConfig.from_env()
        self._client = gcloud_logging.Client(project=self.config.project_id)
        self._logger = self._client.logger(self.config.logger_name)
        self._service = logging_v2.LoggingServiceV2Client()

    def write_structured_event(self, record: LogRecord) -> Dict[str, Any]:
        self._logger.log_struct(record.to_structured_payload(), severity=record.severity)
        return {"project_id": self.config.project_id, "logger": self.config.logger_name, "status": "written"}

    def write_entries(self, records: Iterable[LogRecord]) -> Dict[str, Any]:
        entries = []
        for record in records:
            entries.append(
                {
                    "jsonPayload": record.to_structured_payload(),
                    "severity": record.severity,
                    "labels": record.labels or {},
                    "timestamp": record.timestamp or datetime.now(timezone.utc).isoformat(),
                }
            )
        self._client.batch().commit(entries)
        return {"project_id": self.config.project_id, "count": len(entries), "status": "written"}

    def query(self, query: LogQuery) -> QueryResult:
        filter_expr = query.to_filter()
        resource_names = [f"projects/{self.config.project_id}"]
        response = self._service.list_log_entries(
            resource_names=resource_names,
            filter=filter_expr,
            order_by="timestamp desc",
            page_size=query.limit,
        )
        records = []
        for entry in response:
            payload = dict(entry.json_payload) if entry.json_payload else {}
            records.append(
                LogRecord(
                    message=payload.get("message", ""),
                    severity=entry.severity.name if entry.severity else query.severity or "DEFAULT",
                    timestamp=entry.timestamp.isoformat() if entry.timestamp else None,
                    labels=dict(entry.labels),
                    correlation_id=payload.get("correlation_id"),
                    fields=payload,
                )
            )
        return QueryResult(records=records, filter_expression=filter_expr)

    def recent(self, field_name: str, field_value: str, minutes: int = 60, limit: int = 20) -> QueryResult:
        query = LogQuery(field_name=field_name, field_value=field_value, minutes=minutes, limit=limit)
        return self.query(query)

    def query_errors(self, severity: str = "ERROR", minutes: int = 60, limit: int = 50) -> QueryResult:
        query = LogQuery(severity=severity, minutes=minutes, limit=limit)
        return self.query(query)


def build_client() -> ObservabilityClient:
    return ObservabilityClient()


def normalize_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {normalize_log_name(k): v for k, v in fields.items()}
