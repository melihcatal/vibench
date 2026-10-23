"""Local configuration and client helper utilities for Datadog Logs API."""

import os
from datetime import datetime, timezone, timedelta
from typing import Optional

import requests


DD_API_KEY = os.environ.get("DD_API_KEY", "")
DD_APP_KEY = os.environ.get("DD_APP_KEY", "")
DD_SITE = os.environ.get("DD_SITE", "datadoghq.com")

LOGS_INTAKE_URL = f"https://http-intake.logs.{DD_SITE}/api/v2/logs"
LOGS_QUERY_URL = f"https://api.{DD_SITE}/api/v2/logs/events/search"
LOGS_TAIL_URL = f"https://api.{DD_SITE}/api/v2/logs/events"


def build_log_intake_headers() -> dict:
    """Build headers for Datadog Log Intake API."""
    return {
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def build_logs_query_headers() -> dict:
    """Build headers for Datadog Logs Query API."""
    return {
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def get_time_range(
    minutes_ago: int = 60,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> tuple[str, str]:
    """Return ISO 8601 formatted from/to timestamps for Datadog queries."""
    now = end_time or datetime.now(timezone.utc)
    start = start_time or (now - timedelta(minutes=minutes_ago))
    return start.isoformat(), now.isoformat()


def send_logs_to_datadog(payload: list[dict]) -> requests.Response:
    """Send structured log entries to Datadog Log Intake endpoint."""
    headers = build_log_intake_headers()
    response = requests.post(LOGS_INTAKE_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response


def query_datadog_logs(
    query: str,
    from_time: str,
    to_time: str,
    sort: str = "timestamp",
    limit: int = 100,
) -> requests.Response:
    """Query Datadog Logs Search API with filter, time range, and pagination."""
    headers = build_logs_query_headers()
    body = {
        "filter": {
            "query": query,
            "from": from_time,
            "to": to_time,
        },
        "sort": sort,
        "page": {
            "limit": limit,
        },
    }
    response = requests.post(LOGS_QUERY_URL, json=body, headers=headers, timeout=30)
    response.raise_for_status()
    return response


def tail_datadog_logs(
    query: str,
    from_time: str,
    to_time: str,
    limit: int = 100,
) -> requests.Response:
    """Tail recent Datadog log events with a filter and time range."""
    headers = build_logs_query_headers()
    body = {
        "filter": {
            "query": query,
            "from": from_time,
            "to": to_time,
        },
        "page": {
            "limit": limit,
        },
    }
    response = requests.post(LOGS_TAIL_URL, json=body, headers=headers, timeout=30)
    response.raise_for_status()
    return response
