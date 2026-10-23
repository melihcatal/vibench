"""
Local configuration and client helper utilities for Managed Log Query / Log Ingestion.

Uses Datadog Logs API as the concrete managed logging provider.
Reference: https://docs.datadoghq.com/api/latest/logs/
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from observability_models import (
    LogEvent,
    LogQueryParams,
    LogQueryResponse,
    normalize_log_event,
    parse_datadog_log_entry,
)

DATADOG_API_HOST = "api.datadoghq.com"
DATADOG_API_BASE = "https://api.datadoghq.com/api/v2"


def get_datadog_api_key() -> str:
    """Retrieve the Datadog API key from environment."""
    api_key = os.environ.get("DD_API_KEY")
    if not api_key:
        raise ValueError("DD_API_KEY environment variable is required")
    return api_key


def get_datadog_app_key() -> str:
    """Retrieve the Datadog application key from environment."""
    app_key = os.environ.get("DD_APP_KEY")
    if not app_key:
        raise ValueError("DD_APP_KEY environment variable is required")
    return app_key


def create_datadog_session() -> requests.Session:
    """Create a configured requests session for Datadog API calls."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "DD-API-KEY": get_datadog_api_key(),
            "DD-APPLICATION-KEY": get_datadog_app_key(),
        }
    )
    return session


def build_time_range(
    from_minutes_ago: int = 60, to_minutes_ago: int = 0
) -> tuple[str, str]:
    """Build ISO 8601 time range strings for Datadog queries.

    Returns (from_iso, to_iso) in milliseconds.
    """
    now = datetime.now(timezone.utc)
    from_time = now - timedelta(minutes=from_minutes_ago)
    to_time = now - timedelta(minutes=to_minutes_ago)
    return (
        from_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        to_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    )


def send_log_to_datadog(session: requests.Session, event: LogEvent) -> dict:
    """Send a single structured log event to Datadog Logs Ingestion API.

    Reference endpoint: POST /api/v2/logs
    """
    payload = normalize_log_event(event)
    response = session.post(
        f"{DATADOG_API_BASE}/logs",
        json={"ddsource": payload.get("ddsource", "python"), "ddtags": payload.get("ddtags", ""), "hostname": payload.get("hostname", ""), "message": payload.get("message", ""), "service": payload.get("service", ""), "status": payload.get("status", "info"), "timestamp": payload.get("timestamp")},
    )
    response.raise_for_status()
    return response.json() if response.content else {}


def send_correlated_logs(
    session: requests.Session, events: list[LogEvent], correlation_id: str
) -> list[dict]:
    """Send multiple correlated log events sharing a correlation identifier."""
    results = []
    for event in events:
        event.attributes["correlation_id"] = correlation_id
        event.attributes["request_id"] = correlation_id
        result = send_log_to_datadog(session, event)
        results.append(result)
    return results


def query_datadog_logs(
    session: requests.Session, params: LogQueryParams
) -> LogQueryResponse:
    """Query Datadog Logs API with filter, time range, and pagination.

    Reference endpoint: POST /api/v2/logs/events/search
    """
    from_iso, to_iso = build_time_range(
        params.from_minutes_ago, params.to_minutes_ago
    )

    query_filter = {
        "query": params.query_string,
        "time": {"from": from_iso, "to": to_iso},
    }

    payload = {
        "filter": query_filter,
        "sort": params.sort_order,
        "page": {"limit": params.page_size, "cursor": params.cursor},
    }

    response = session.post(
        f"{DATADOG_API_BASE}/logs/events/search",
        json=payload,
    )
    response.raise_for_status()
    data = response.json()

    entries = []
    for entry in data.get("data", []):
        parsed = parse_datadog_log_entry(entry)
        entries.append(parsed)

    next_cursor = data.get("meta", {}).get("page", {}).get("after", None)

    return LogQueryResponse(
        logs=entries,
        cursor=next_cursor,
        total_count=len(entries),
    )
