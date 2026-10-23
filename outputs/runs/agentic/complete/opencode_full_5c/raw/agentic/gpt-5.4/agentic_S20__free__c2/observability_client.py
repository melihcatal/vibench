from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests

from observability_models import LogEvent, LogQueryRequest, normalize_datadog_log


DATADOG_LOGS_BASE_URL = os.getenv(
    "DATADOG_LOGS_BASE_URL", "https://http-intake.logs.datadoghq.com"
)
DATADOG_API_BASE_URL = os.getenv("DATADOG_API_BASE_URL", "https://api.datadoghq.com")
DATADOG_API_KEY_ENV = "DATADOG_API_KEY"
DATADOG_APP_KEY_ENV = "DATADOG_APP_KEY"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _headers(include_app_key: bool = False) -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": require_env(DATADOG_API_KEY_ENV),
    }
    if include_app_key:
        headers["DD-APPLICATION-KEY"] = require_env(DATADOG_APP_KEY_ENV)
    return headers


def logs_intake_url() -> str:
    return f"{DATADOG_LOGS_BASE_URL.rstrip('/')}/api/v2/logs"


def logs_search_url() -> str:
    return f"{DATADOG_API_BASE_URL.rstrip('/')}/api/v2/logs/events/search"


def send_logs(events: Iterable[LogEvent], timeout: int = 30) -> Dict[str, Any]:
    payload = [event.to_datadog_log() for event in events]
    response = requests.post(
        logs_intake_url(), headers=_headers(), json=payload, timeout=timeout
    )
    response.raise_for_status()
    if response.content:
        return response.json()
    return {"status": "ok", "count": len(payload)}


def query_logs(request: LogQueryRequest, timeout: int = 30) -> List[Dict[str, Any]]:
    response = requests.post(
        logs_search_url(),
        headers=_headers(include_app_key=True),
        json=request.to_datadog_body(),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


def query_normalized_logs(
    request: LogQueryRequest, timeout: int = 30
) -> List[Dict[str, Any]]:
    items = query_logs(request=request, timeout=timeout)
    normalized = []
    for item in items:
        record = normalize_datadog_log(item)
        normalized.append(
            {
                "timestamp": record.timestamp,
                "service": record.service,
                "severity": record.severity,
                "message": record.message,
                "correlation_id": record.correlation_id,
                "attributes": record.attributes,
            }
        )
    return normalized


def time_window(last_minutes: int) -> Dict[str, str]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=last_minutes)
    return {"start": start_time.isoformat(), "end": end_time.isoformat()}


def build_query(*parts: Optional[str]) -> str:
    return " ".join(part for part in parts if part)
