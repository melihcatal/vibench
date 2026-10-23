from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional

import requests

from observability_models import (
    LogEvent,
    LogQueryRequest,
    NormalizedLogQueryResponse,
    normalize_datadog_logs_response,
)


DATADOG_SITE = os.getenv("DD_SITE", "datadoghq.com")
DATADOG_LOGS_BASE_URL = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"
DATADOG_LOGS_SEARCH_URL = f"https://api.{DATADOG_SITE}/api/v2/logs/events/search"


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key or os.environ["DD_API_KEY"]
        self.app_key = app_key or os.environ["DD_APP_KEY"]
        self.timeout = timeout

    def _ingest_headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

    def _query_headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        response = requests.post(
            DATADOG_LOGS_BASE_URL,
            headers=self._ingest_headers(),
            json=event.to_datadog(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        if not response.content:
            return {"status": "accepted"}
        return response.json()

    def write_logs(self, events: Iterable[LogEvent]) -> Dict[str, Any]:
        payload: List[Dict[str, Any]] = [event.to_datadog() for event in events]
        response = requests.post(
            DATADOG_LOGS_BASE_URL,
            headers=self._ingest_headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if not response.content:
            return {"status": "accepted", "count": len(payload)}
        return response.json()

    def query_logs(self, request: LogQueryRequest) -> NormalizedLogQueryResponse:
        response = requests.post(
            DATADOG_LOGS_SEARCH_URL,
            headers=self._query_headers(),
            json=request.to_datadog(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_datadog_logs_response(response.json())


def build_error_query(service: Optional[str], severity: str) -> str:
    parts = [f"status:{severity.lower()}"]
    if service:
        parts.append(f"service:{service}")
    return " ".join(parts)


def build_field_query(filters: Optional[Dict[str, Any]] = None) -> str:
    filters = filters or {}
    clauses = []
    for key, value in filters.items():
        clauses.append(f"@{key}:{value}")
    return " ".join(clauses) if clauses else "*"
