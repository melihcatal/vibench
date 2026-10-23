from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional

import requests

from observability_models import LogQueryRequest, LogQueryResponse, StructuredLogEvent, normalize_datadog_log_item


DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")
DATADOG_LOGS_INTAKE_URL = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"
DATADOG_LOGS_SEARCH_URL = f"https://api.{DATADOG_SITE}/api/v2/logs/events/search"


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key or DATADOG_API_KEY
        self.app_key = app_key or DATADOG_APP_KEY
        self.site = site or DATADOG_SITE
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("DATADOG_API_KEY is required")

    @property
    def intake_url(self) -> str:
        return f"https://http-intake.logs.{self.site}/api/v2/logs"

    @property
    def search_url(self) -> str:
        return f"https://api.{self.site}/api/v2/logs/events/search"

    def _intake_headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

    def _search_headers(self) -> Dict[str, str]:
        if not self.app_key:
            raise ValueError("DATADOG_APP_KEY is required for log queries")
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def submit_log(self, event: StructuredLogEvent) -> Dict[str, Any]:
        response = requests.post(
            self.intake_url,
            headers=self._intake_headers(),
            json=[event.to_datadog_log()],
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": "accepted"}

    def submit_logs(self, events: Iterable[StructuredLogEvent]) -> Dict[str, Any]:
        payload: List[Dict[str, Any]] = [event.to_datadog_log() for event in events]
        response = requests.post(
            self.intake_url,
            headers=self._intake_headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"status": "accepted", "count": len(payload)}

    def search_logs(self, request: LogQueryRequest) -> LogQueryResponse:
        response = requests.post(
            self.search_url,
            headers=self._search_headers(),
            json=request.to_datadog_payload(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        raw = response.json()
        records = [normalize_datadog_log_item(item) for item in raw.get("data", [])]
        return LogQueryResponse(records=records, raw=raw)
