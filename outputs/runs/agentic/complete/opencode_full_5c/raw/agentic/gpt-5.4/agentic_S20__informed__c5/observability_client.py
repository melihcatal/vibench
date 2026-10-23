from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests

from observability_models import (
    CorrelatedLogBatch,
    LogEvent,
    LogQueryRequest,
    NormalizedLogRecord,
    normalize_datadog_log,
)


class DatadogLogsClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.environ["DD_API_KEY"]
        self.app_key = app_key or os.environ["DD_APP_KEY"]
        self.site = site or os.environ.get("DD_SITE", "datadoghq.com")
        self.logs_intake_url = f"https://http-intake.logs.{self.site}/api/v2/logs"
        self.logs_search_url = f"https://api.{self.site}/api/v2/logs/events/search"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        response = self.session.post(
            self.logs_intake_url, json=[event.to_datadog_http()], timeout=30
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": "accepted", "provider": "Datadog Logs API"}

    def write_logs(self, batch: CorrelatedLogBatch) -> Dict[str, Any]:
        response = self.session.post(
            self.logs_intake_url, json=batch.to_datadog_http(), timeout=30
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {
            "status": "accepted",
            "provider": "Datadog Logs API",
            "request_id": batch.request_id,
        }

    def search_logs(self, request: LogQueryRequest) -> List[NormalizedLogRecord]:
        response = self.session.post(
            self.logs_search_url, json=request.to_datadog_payload(), timeout=30
        )
        response.raise_for_status()
        payload = response.json()
        return [normalize_datadog_log(item) for item in payload.get("data", [])]


def build_log_event(
    message: str,
    service: str,
    source: str,
    host: str,
    status: str = "info",
    tags: Optional[List[str]] = None,
    attributes: Optional[Dict[str, Any]] = None,
) -> LogEvent:
    return LogEvent(
        message=message,
        service=service,
        source=source,
        host=host,
        status=status,
        tags=tags or [],
        attributes=attributes or {},
    )
