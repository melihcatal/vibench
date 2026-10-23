import os
from typing import Any, Dict, List, Optional

import requests

from observability_models import LogEvent, LogQuery, LogResponse


def get_datadog_config() -> Dict[str, str]:
    return {
        "api_key": os.environ.get("DD_API_KEY", ""),
        "app_key": os.environ.get("DD_APP_KEY", ""),
        "site": os.environ.get("DD_SITE", "datadoghq.com"),
        "service": os.environ.get("DD_SERVICE", "orders-api"),
    }


def datadog_headers() -> Dict[str, str]:
    cfg = get_datadog_config()
    return {
        "DD-API-KEY": cfg["api_key"],
        "DD-APPLICATION-KEY": cfg["app_key"],
        "Content-Type": "application/json",
    }


def _base_url() -> str:
    return f"https://api.{get_datadog_config()['site']}"


def send_log(event: LogEvent) -> Dict[str, Any]:
    payload = {"logs": [event.to_dict()]}
    resp = requests.post(
        f"{_base_url()}/api/v2/logs",
        headers=datadog_headers(),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return {
        "status_code": resp.status_code,
        "body": resp.json() if resp.content else {},
    }


def search_logs(query: LogQuery) -> LogResponse:
    payload = {
        "filter": {
            "query": query.query,
            "from": query.start_time,
            "to": query.end_time,
        },
        "page": {"limit": query.limit},
    }
    if query.severity:
        payload["filter"]["query"] = f"{query.query} severity:{query.severity}"
    resp = requests.post(
        f"{_base_url()}/api/v2/logs/events/search",
        headers=datadog_headers(),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return LogResponse(items=data.get("data", []), provider="Datadog")


def recent_logs(
    field: str, value: str, start_time: str, end_time: str, limit: int = 50
) -> LogResponse:
    return search_logs(
        LogQuery(
            query=f"{field}:{value}",
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )
    )
