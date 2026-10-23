from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional

import requests

from observability_models import LogQueryRequest, LogQueryResponse, normalize_datadog_logs


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key or os.environ["DD_API_KEY"]
        self.app_key = app_key or os.environ["DD_APP_KEY"]
        self.site = site or os.getenv("DD_SITE", "datadoghq.com")
        self.timeout = timeout
        self.logs_intake_url = f"https://http-intake.logs.{self.site}/api/v2/logs"
        self.logs_search_url = f"https://api.{self.site}/api/v2/logs/events/search"

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def send_logs(self, events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        payload = list(events)
        response = requests.post(
            self.logs_intake_url,
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": response.status_code}

    def search_logs(self, request: LogQueryRequest) -> LogQueryResponse:
        response = requests.post(
            self.logs_search_url,
            headers=self._headers(),
            json=request.to_datadog_payload(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        raw = response.json()
        return LogQueryResponse(records=normalize_datadog_logs(raw.get("data", [])), raw=raw)


def build_log_query(
    *,
    query: str,
    from_time: str,
    to_time: str,
    limit: int = 50,
    sort: str = "desc",
) -> LogQueryRequest:
    return LogQueryRequest(
        query=query,
        from_time=from_time,
        to_time=to_time,
        limit=limit,
        sort=sort,
    )


def join_field_filters(filters: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key, value in filters.items():
        if isinstance(value, str) and " " in value:
            parts.append(f"@{key}:\"{value}\"")
        else:
            parts.append(f"@{key}:{value}")
    return " ".join(parts)
