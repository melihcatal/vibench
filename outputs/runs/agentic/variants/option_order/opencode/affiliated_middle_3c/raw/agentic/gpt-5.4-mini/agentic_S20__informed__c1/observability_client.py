import os
from typing import Any, Dict, List, Optional

import requests

from observability_models import (
    LogQueryResult,
    LogWriteResult,
    build_log_event,
    extract_items,
    normalize_query_filters,
)


DATADOG_LOGS_API_HOST = os.getenv(
    "DATADOG_LOGS_API_HOST", "https://http-intake.logs.datadoghq.com"
)


def _headers() -> Dict[str, str]:
    return {
        "DD-API-KEY": os.environ["DD_API_KEY"],
        "DD-APPLICATION-KEY": os.environ["DD_APP_KEY"],
        "Content-Type": "application/json",
    }


def write_log_event(
    message: str, severity: str = "INFO", **fields: Any
) -> LogWriteResult:
    payload = build_log_event(message, severity, **fields)
    response = requests.post(
        f"{DATADOG_LOGS_API_HOST}/api/v2/logs",
        headers=_headers(),
        json=[payload],
        timeout=30,
    )
    response.raise_for_status()
    request_id = response.headers.get("x-request-id") or response.headers.get(
        "x-datadog-request-id"
    )
    return LogWriteResult(
        success=True,
        request_id=request_id,
        raw=response.json() if response.content else None,
    )


def query_logs(
    query: str,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 50,
) -> LogQueryResult:
    params = normalize_query_filters(
        {
            "filter[query]": query,
            "filter[from]": time_from,
            "filter[to]": time_to,
            "page[limit]": limit,
            **(filters or {}),
        }
    )
    response = requests.get(
        "https://api.datadoghq.com/api/v2/logs/events/search",
        headers=_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json() if response.content else {}
    return LogQueryResult(items=extract_items(payload), raw=payload)


def fetch_recent_logs(
    field_filters: Optional[Dict[str, Any]] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 50,
) -> LogQueryResult:
    filters = normalize_query_filters(field_filters)
    query = " ".join(f"{k}:{v}" for k, v in filters.items()) if filters else "*"
    return query_logs(
        query=query,
        time_from=time_from,
        time_to=time_to,
        filters={"page[limit]": limit},
        limit=limit,
    )
