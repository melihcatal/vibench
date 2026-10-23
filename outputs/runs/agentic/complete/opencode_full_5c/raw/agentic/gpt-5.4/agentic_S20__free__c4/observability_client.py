from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional
import os

import requests

from observability_models import (
    LogEvent,
    LogQuery,
    LogQueryResponse,
    normalize_datadog_search_response,
)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def datadog_site() -> str:
    return os.getenv("DATADOG_SITE", "datadoghq.com")


def datadog_api_key() -> str:
    return _require_env("DATADOG_API_KEY")


def datadog_app_key() -> str:
    return _require_env("DATADOG_APP_KEY")


def logs_intake_url() -> str:
    return f"https://http-intake.logs.{datadog_site()}/api/v2/logs"


def logs_search_url() -> str:
    return f"https://api.{datadog_site()}/api/v2/logs/events/search"


def iso_utc_minutes_ago(minutes: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class DatadogObservabilityClient:
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout

    def _intake_headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": datadog_api_key(),
            "Content-Type": "application/json",
        }

    def _search_headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": datadog_api_key(),
            "DD-APPLICATION-KEY": datadog_app_key(),
            "Content-Type": "application/json",
        }

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        response = requests.post(
            logs_intake_url(),
            headers=self._intake_headers(),
            json=[event.to_datadog_log()],
            timeout=self.timeout,
        )
        response.raise_for_status()
        return {"status_code": response.status_code, "accepted": True}

    def write_logs(self, events: Iterable[LogEvent]) -> Dict[str, Any]:
        payload = [event.to_datadog_log() for event in events]
        response = requests.post(
            logs_intake_url(),
            headers=self._intake_headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return {
            "status_code": response.status_code,
            "accepted": True,
            "count": len(payload),
        }

    def search_logs(self, query: LogQuery) -> LogQueryResponse:
        payload = {
            "filter": {
                "query": query.query,
                "from": query.from_time,
                "to": query.to_time,
            },
            "sort": query.sort,
            "page": {"limit": query.limit},
        }
        response = requests.post(
            logs_search_url(),
            headers=self._search_headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_datadog_search_response(response.json())


def build_field_query(field_filters: Optional[Dict[str, Any]] = None) -> str:
    if not field_filters:
        return "*"
    parts: List[str] = []
    for key, value in field_filters.items():
        if isinstance(value, str) and " " in value:
            parts.append(f'{key}:"{value}"')
        else:
            parts.append(f"{key}:{value}")
    return " AND ".join(parts) if parts else "*"
