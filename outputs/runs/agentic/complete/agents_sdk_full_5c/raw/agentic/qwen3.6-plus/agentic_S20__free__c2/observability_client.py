"""Provide local configuration and client helper utilities for Managed Log Query / Log Ingestion using Datadog."""

import os
from datetime import datetime, timezone, timedelta
from typing import Optional, Any

from datadog_api_client import Configuration
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.api.logs_indexes_api import LogsIndexesApi
from datadog_api_client.v1.model.http_log import HTTPLog
from datadog_api_client.v1.model.http_log_item import HTTPLogItem

from observability_models import LogEvent, LogQueryRequest, LogQueryResponse


def get_datadog_configuration() -> Configuration:
    """Build a Datadog API Configuration from environment variables."""
    config = Configuration()
    api_key = os.environ.get("DD_API_KEY", "")
    app_key = os.environ.get("DD_APP_KEY", "")
    dd_site = os.environ.get("DD_SITE", "datadoghq.com")

    if not api_key:
        raise ValueError("DD_API_KEY environment variable is required")

    config.api_key = {"apiKeyAuth": api_key}
    if app_key:
        config.api_key["appKeyAuth"] = app_key
    config.server_variables = {"site": dd_site}
    return config


def get_logs_api() -> LogsApi:
    """Create and return a configured Datadog LogsApi client."""
    config = get_datadog_configuration()
    return LogsApi(config)


def get_logs_indexes_api() -> LogsIndexesApi:
    """Create and return a configured Datadog LogsIndexesApi client."""
    config = get_datadog_configuration()
    return LogsIndexesApi(config)


def log_event_to_http_log_items(events: list[LogEvent]) -> list[HTTPLogItem]:
    """Convert normalized LogEvent objects to Datadog HTTPLogItem payloads."""
    items = []
    for event in events:
        payload = event.to_dict()
        item = HTTPLogItem(
            hostname=payload.get("hostname", ""),
            service=payload.get("service", ""),
            ddsource=payload.get("ddsource", ""),
            message=payload.get("message", ""),
            ddtags=payload.get("tags", ""),
            status=payload.get("status", "info"),
        )
        # Attach custom attributes as additional fields
        for k, v in payload.items():
            if k not in ("hostname", "service", "ddsource", "message", "ddtags", "status", "timestamp"):
                setattr(item, k, v)
        items.append(item)
    return items


def submit_logs(events: list[LogEvent]) -> dict:
    """Submit a batch of LogEvent objects to Datadog log ingestion endpoint."""
    api = get_logs_api()
    items = log_event_to_http_log_items(events)
    response = api.submit_log(logs=items)
    return response


def compute_time_range(minutes: int = 30) -> tuple[int, int]:
    """Compute epoch-second from/to timestamps for the last N minutes."""
    now = datetime.now(timezone.utc)
    to_ts = int(now.timestamp())
    from_ts = int((now - timedelta(minutes=minutes)).timestamp())
    return from_ts, to_ts


def parse_log_response(response: Any) -> LogQueryResponse:
    """Parse a Datadog API response into a normalized LogQueryResponse."""
    if response is None:
        return LogQueryResponse()
    data = response.get("data", []) if isinstance(response, dict) else []
    logs = []
    for entry in data:
        attrs = entry.get("attributes", {})
        logs.append({
            "message": attrs.get("message", ""),
            "status": attrs.get("status", "unknown"),
            "service": attrs.get("service", ""),
            "timestamp": attrs.get("timestamp", ""),
            "hostname": attrs.get("host", ""),
            "attributes": attrs.get("attributes", {}),
            "tags": attrs.get("tags", []),
        })
    meta = response.get("meta", {}).get("page", {})
    total = meta.get("total_matched", len(logs))
    next_token = meta.get("after")
    return LogQueryResponse(logs=logs, total_count=total, next_page_token=next_token)
