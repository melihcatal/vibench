import os
import json
import time
from typing import Optional
from datetime import datetime, timezone, timedelta

import requests

from observability_models import (
    LogEvent,
    LogQueryRequest,
    LogQueryResponse,
    LogWriteResponse,
    LogEntry,
    normalize_datadog_log,
)

DATADOG_API_HOST = os.getenv("DATADOG_API_HOST", "api.datadoghq.com")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY", "")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")

LOGS_INTAKE_URL = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"
LOGS_QUERY_URL = f"https://{DATADOG_API_HOST}/api/v2/logs/events/search"


def _build_headers() -> dict[str, str]:
    return {
        "DD-API-KEY": DATADOG_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _build_intake_headers() -> dict[str, str]:
    return {
        "DD-API-KEY": DATADOG_API_KEY,
        "Content-Type": "application/json",
    }


def load_config() -> dict:
    return {
        "api_host": DATADOG_API_HOST,
        "site": DATADOG_SITE,
        "api_key": DATADOG_API_KEY,
        "app_key": DATADOG_APP_KEY,
        "logs_intake_url": LOGS_INTAKE_URL,
        "logs_query_url": LOGS_QUERY_URL,
    }


def send_log_events(events: list[LogEvent]) -> LogWriteResponse:
    payloads = [event.to_datadog_payload() for event in events]
    body = json.dumps(payloads)
    headers = _build_intake_headers()
    resp = requests.post(LOGS_INTAKE_URL, data=body, headers=headers, timeout=30)
    if resp.status_code in (200, 202, 204):
        return LogWriteResponse(success=True, event_count=len(events))
    errors = [f"HTTP {resp.status_code}: {resp.text}"]
    return LogWriteResponse(success=False, errors=errors)


def query_logs(request: LogQueryRequest) -> LogQueryResponse:
    headers = _build_headers()
    body = {
        "filter": {
            "query": request.query,
            "indexes": [request.index],
        },
        "page": {
            "limit": request.limit,
        },
        "sort": request.sort,
    }
    if request.from_ts:
        body["filter"]["from"] = f"{int(request.from_ts.timestamp())}s"
    if request.to_ts:
        body["filter"]["to"] = f"{int(request.to_ts.timestamp())}s"

    resp = requests.post(LOGS_QUERY_URL, json=body, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    entries: list[LogEntry] = []
    for raw in data.get("data", []):
        entries.append(normalize_datadog_log(raw))
    next_page_token = data.get("meta", {}).get("page", {}).get("after")
    total = data.get("meta", {}).get("page", {}).get("total", 0)
    return LogQueryResponse(
        entries=entries, next_page_token=next_page_token, total_count=total
    )


def get_default_time_range(hours: int = 1) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    from_ts = now - timedelta(hours=hours)
    return from_ts, now
