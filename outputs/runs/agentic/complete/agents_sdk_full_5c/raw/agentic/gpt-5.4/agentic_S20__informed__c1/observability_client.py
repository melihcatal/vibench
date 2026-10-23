from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from observability_models import QueryResult, normalize_datadog_search_response


DATADOG_API_BASE = os.getenv("DATADOG_API_BASE", "https://api.datadoghq.com")
DATADOG_LOGS_BASE = os.getenv("DATADOG_LOGS_BASE", "https://http-intake.logs.datadoghq.com")


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        api_base: Optional[str] = None,
        logs_base: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.getenv("DD_API_KEY")
        self.app_key = app_key or os.getenv("DD_APP_KEY")
        self.api_base = (api_base or DATADOG_API_BASE).rstrip("/")
        self.logs_base = (logs_base or DATADOG_LOGS_BASE).rstrip("/")
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("DD_API_KEY is required for Datadog Logs API")

    @property
    def intake_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key,
        }

    @property
    def search_headers(self) -> Dict[str, str]:
        if not self.app_key:
            raise ValueError("DD_APP_KEY is required for Datadog log search")
        return {
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }

    def submit_logs(self, logs: Any) -> Dict[str, Any]:
        response = requests.post(
            f"{self.logs_base}/api/v2/logs",
            headers=self.intake_headers,
            json=logs,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": "accepted", "provider": "datadog"}

    def search_logs(self, payload: Dict[str, Any]) -> QueryResult:
        response = requests.post(
            f"{self.api_base}/api/v2/logs/events/search",
            headers=self.search_headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return normalize_datadog_search_response(response.json())


def build_time_range(start: str, end: str) -> Dict[str, str]:
    return {"from": start, "to": end}


def build_search_payload(filter_query: str, start: str, end: str, limit: int = 50) -> Dict[str, Any]:
    return {
        "filter": {
            "query": filter_query,
            **build_time_range(start, end),
        },
        "sort": "timestamp",
        "page": {"limit": limit},
    }
