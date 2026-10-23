import os
import time
import requests
from typing import Optional
from datetime import datetime, timezone, timedelta

from observability_models import (
    LogEvent,
    LogQueryRequest,
    LogQueryResponse,
    IngestionResponse,
)


DATADOG_LOGS_INGEST_URL = "https://http-intake.logs.datadoghq.com/api/v2/logs"
DATADOG_LOGS_QUERY_URL = "https://api.datadoghq.com/api/v2/logs/events/search"


def get_dd_api_key() -> str:
    api_key = os.environ.get("DD_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DD_API_KEY environment variable is required for Datadog Logs API"
        )
    return api_key


def get_dd_app_key() -> str:
    app_key = os.environ.get("DD_APP_KEY")
    if not app_key:
        raise RuntimeError(
            "DD_APP_KEY environment variable is required for Datadog Logs API"
        )
    return app_key


def get_dd_site() -> str:
    return os.environ.get("DD_SITE", "datadoghq.com")


def build_ingest_url() -> str:
    site = get_dd_site()
    return f"https://http-intake.logs.{site}/api/v2/logs"


def build_query_url() -> str:
    site = get_dd_site()
    return f"https://api.{site}/api/v2/logs/events/search"


def build_ingest_headers() -> dict[str, str]:
    return {
        "DD-API-KEY": get_dd_api_key(),
        "Content-Type": "application/json",
    }


def build_query_headers() -> dict[str, str]:
    return {
        "DD-API-KEY": get_dd_api_key(),
        "DD-APPLICATION-KEY": get_dd_app_key(),
        "Content-Type": "application/json",
    }


def ingest_log_events(
    events: list[LogEvent],
    ddtags: Optional[str] = None,
) -> IngestionResponse:
    url = build_ingest_url()
    headers = build_ingest_headers()

    payloads = []
    for event in events:
        payload = event.to_dict()
        if ddtags:
            existing = payload.get("ddtags", "")
            payload["ddtags"] = f"{ddtags},{existing}" if existing else ddtags
        payloads.append(payload)

    body = {"logs": payloads}

    response = requests.post(url, headers=headers, json=body, timeout=30)
    resp_body = response.json() if response.content else {}
    return IngestionResponse.from_datadog_response(response.status_code, resp_body)


def query_logs(request: LogQueryRequest) -> LogQueryResponse:
    url = build_query_url()
    headers = build_query_headers()
    params = request.to_params()

    response = requests.post(
        url, headers=headers, json={"data": {"attributes": params}}, timeout=60
    )
    resp_body = response.json() if response.content else {}
    return LogQueryResponse.from_datadog_response(resp_body)


def build_time_range(minutes_ago: int = 30) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    time_from = (now - timedelta(minutes=minutes_ago)).isoformat()
    time_to = now.isoformat()
    return time_from, time_to


def build_error_query(
    service: Optional[str] = None,
    source: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra_filters: Optional[str] = None,
) -> str:
    parts = ["status:error OR status:critical OR status:alert OR status:emergency"]
    if service:
        parts.append(f"service:{service}")
    if source:
        parts.append(f"source:{source}")
    if correlation_id:
        parts.append(f"correlation_id:{correlation_id}")
    if extra_filters:
        parts.append(extra_filters)
    return " AND ".join(parts)


def build_field_query(
    field_filters: dict[str, str],
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
) -> LogQueryRequest:
    parts = []
    for field_name, field_value in field_filters.items():
        parts.append(f"{field_name}:{field_value}")
    query = " AND ".join(parts) if parts else "*"
    tf, tt = build_time_range()
    return LogQueryRequest(
        query=query,
        time_from=time_from or tf,
        time_to=time_to or tt,
    )
