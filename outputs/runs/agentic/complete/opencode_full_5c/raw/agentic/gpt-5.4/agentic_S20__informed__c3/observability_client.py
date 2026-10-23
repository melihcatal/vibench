from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import os

import requests

from observability_models import (
    LogEvent,
    LogQuery,
    NormalizedLogEntry,
    normalize_datadog_log,
)


DATADOG_API_BASE = os.getenv("DATADOG_API_BASE", "https://api.datadoghq.com")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")


def _api_base() -> str:
    if DATADOG_API_BASE:
        return DATADOG_API_BASE.rstrip("/")
    return f"https://api.{DATADOG_SITE}"


def _headers() -> Dict[str, str]:
    api_key = os.environ["DD_API_KEY"]
    app_key = os.environ.get("DD_APP_KEY", "")
    headers = {
        "DD-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    if app_key:
        headers["DD-APPLICATION-KEY"] = app_key
    return headers


class DatadogObservabilityClient:
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
        self.session = requests.Session()

    def ingest_logs(self, events: List[LogEvent]) -> Dict[str, Any]:
        payload = [event.to_record() for event in events]
        response = self.session.post(
            f"{_api_base()}/api/v2/logs",
            headers=_headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": response.status_code}

    def search_logs(self, query: LogQuery) -> List[NormalizedLogEntry]:
        body = {
            "filter": {
                "from": query.start_time,
                "to": query.end_time,
                "query": query.query,
            },
            "sort": "timestamp",
            "page": {"limit": query.limit},
        }
        response = self.session.post(
            f"{_api_base()}/api/v2/logs/events/search",
            headers=_headers(),
            json=body,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return [normalize_datadog_log(item) for item in data]


def iso_utc_minutes_ago(minutes: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_field_query(filters: Optional[Dict[str, Any]] = None) -> str:
    if not filters:
        return "*"
    parts: List[str] = []
    for key, value in filters.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            joined = " OR ".join(f"@{key}:{item}" for item in value)
            parts.append(f"({joined})")
        else:
            parts.append(f"@{key}:{value}")
    return " AND ".join(parts) if parts else "*"
