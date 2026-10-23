from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from google.cloud import logging as gcloud_logging
from google.cloud.logging_v2.handlers.handlers import CloudLoggingHandler
from google.cloud.logging_v2.resource import Resource

from observability_models import LogEvent, LogQuery


@dataclass(slots=True)
class ObservabilityConfig:
    project_id: str | None = None
    log_name: str = "application"

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
            log_name=os.getenv("LOG_NAME", "application"),
        )


class ObservabilityClient:
    def __init__(self, config: ObservabilityConfig | None = None):
        self.config = config or ObservabilityConfig.from_env()
        self.client = gcloud_logging.Client(project=self.config.project_id)
        self.logger = self.client.logger(self.config.log_name)

    def write_event(self, event: LogEvent) -> dict[str, Any]:
        payload = event.normalized()
        self.logger.log_struct(payload, severity=event.severity.upper())
        return payload

    def write_text(self, message: str, severity: str = "INFO", **fields: Any) -> dict[str, Any]:
        event = LogEvent(message=message, severity=severity, fields=fields)
        return self.write_event(event)

    def query_entries(self, query: LogQuery) -> list[dict[str, Any]]:
        filters = [f'timestamp >= "{query.start_time.isoformat()}"', f'timestamp <= "{query.end_time.isoformat()}"']
        if query.severity:
            filters.append(f'severity >= {query.severity.upper()}')
        for key, value in query.field_filters.items():
            filters.append(f'{key} = "{value}"')
        entries = self.client.list_entries(filter_=" AND ".join(filters), order_by=gcloud_logging.DESCENDING, max_results=query.limit)
        return [self._entry_to_dict(entry) for entry in entries]

    @staticmethod
    def _entry_to_dict(entry: Any) -> dict[str, Any]:
        payload = dict(getattr(entry, "payload", {}) or {})
        payload["timestamp"] = getattr(entry, "timestamp", None).isoformat() if getattr(entry, "timestamp", None) else None
        payload["severity"] = getattr(entry, "severity", None)
        payload["log_name"] = getattr(entry, "log_name", None)
        return payload


class CloudLoggingContext:
    def __init__(self, client: ObservabilityClient):
        self.client = client

    def __enter__(self) -> ObservabilityClient:
        return self.client

    def __exit__(self, exc_type, exc, tb) -> None:
        return None
