import os
import json
from typing import Any, Optional

import requests

from observability_models import (
    LogEvent,
    LogQueryRequest,
    LogQueryResponse,
)


DATADOG_LOG_INGEST_ENDPOINT = "https://http-intake.logs.datadoghq.com/v1/input"
DATADOG_LOG_QUERY_ENDPOINT = "https://api.datadoghq.com/api/v2/logs/events/search"


def get_datadog_api_key() -> str:
    api_key = os.environ.get("DATADOG_API_KEY", "")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY environment variable is required")
    return api_key


def get_datadog_app_key() -> str:
    app_key = os.environ.get("DATADOG_APP_KEY", "")
    if not app_key:
        raise RuntimeError("DATADOG_APP_KEY environment variable is required")
    return app_key


def get_datadog_site() -> str:
    return os.environ.get("DATADOG_SITE", "datadoghq.com")


def build_ingest_headers() -> dict[str, str]:
    api_key = get_datadog_api_key()
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
    }


def build_query_headers() -> dict[str, str]:
    api_key = get_datadog_api_key()
    app_key = get_datadog_app_key()
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


def ingest_log_event(event: LogEvent) -> dict[str, Any]:
    headers = build_ingest_headers()
    payload = event.to_dict()
    resp = requests.post(
        DATADOG_LOG_INGEST_ENDPOINT, headers=headers, json=payload, timeout=30
    )
    resp.raise_for_status()
    return resp.json() if resp.content else {}


def ingest_correlated_logs(events: list[LogEvent]) -> list[dict[str, Any]]:
    results = []
    for event in events:
        result = ingest_log_event(event)
        results.append(result)
    return results


def query_logs(request: LogQueryRequest) -> LogQueryResponse:
    headers = build_query_headers()
    body = request.to_datadog_query()
    resp = requests.post(
        DATADOG_LOG_QUERY_ENDPOINT, headers=headers, json=body, timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    return LogQueryResponse.from_datadog_response(data)


def fetch_logs_with_field_filter(
    field_name: str,
    field_value: str,
    time_from: str,
    time_to: str,
    limit: int = 100,
    extra_query: str = "",
) -> LogQueryResponse:
    request = LogQueryRequest(
        query=extra_query,
        time_from=time_from,
        time_to=time_to,
        filter_field=field_name,
        filter_value=field_value,
        limit=limit,
    )
    return query_logs(request)
