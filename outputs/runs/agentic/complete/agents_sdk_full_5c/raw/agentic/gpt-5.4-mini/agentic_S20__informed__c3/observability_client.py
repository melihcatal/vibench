from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any, Iterable

import requests

from observability_models import LogEvent, LogQuery, LogQueryResult, normalize_log_payload

DATADOG_API_HOST = "https://api.datadoghq.com"


def load_datadog_config() -> dict[str, str]:
    return {
        "api_key": os.getenv("DD_API_KEY", ""),
        "app_key": os.getenv("DD_APP_KEY", ""),
        "site": os.getenv("DD_SITE", DATADOG_API_HOST),
        "service": os.getenv("DD_SERVICE", "managed-log-service"),
        "logger_name": os.getenv("DD_LOGGER_NAME", "application"),
    }


class DatadogLogsClient:
    def __init__(self, api_key: str, app_key: str, site: str = DATADOG_API_HOST) -> None:
        self.api_key = api_key
        self.app_key = app_key
        self.site = site.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key,
                "Content-Type": "application/json",
            }
        )

    def write_log(self, event: LogEvent) -> dict[str, Any]:
        url = f"{self.site}/api/v2/logs"
        payload = [normalize_log_payload(event.to_dict())]
        response = self.session.post(url, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        return {"status_code": response.status_code, "response": response.text}

    def query_logs(self, query: LogQuery) -> LogQueryResult:
        url = f"{self.site}/api/v2/logs/events/search"
        search_query = self._build_search_query(query)
        payload = {"filter": {"query": search_query, "from": query.start_time, "to": query.end_time}, "page": {"limit": query.limit}}
        response = self.session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        entries = data.get("data", []) if isinstance(data, dict) else []
        return LogQueryResult(entries=entries, raw_response=data)

    def _build_search_query(self, query: LogQuery) -> str:
        parts: list[str] = []
        if query.severity:
            parts.append(f"severity:{query.severity.upper()}")
        for field, value in query.field_filters.items():
            parts.append(f'{field}:{json.dumps(value).strip("\"")}')
        return " AND ".join(parts) if parts else "*"


def get_client() -> DatadogLogsClient:
    cfg = load_datadog_config()
    return DatadogLogsClient(cfg["api_key"], cfg["app_key"], cfg["site"])


def build_log_event(message: str, severity: str = "INFO", correlation_id: str | None = None, **fields: Any) -> LogEvent:
    return LogEvent(service=load_datadog_config()["service"], severity=severity, message=message, correlation_id=correlation_id, fields=fields)
