from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, LogQuery, LogQueryResult

DATADOG_LOGS_API_BASE = "https://http-intake.logs.datadoghq.com/api/v2"
DATADOG_QUERY_API_BASE = "https://api.datadoghq.com/api/v2"


@dataclass
class ObservabilityConfig:
    dd_api_key: str
    dd_app_key: str
    site: str = "datadoghq.com"

    @property
    def intake_url(self) -> str:
        if self.site == "datadoghq.eu":
            return "https://http-intake.logs.datadoghq.eu/api/v2"
        return DATADOG_LOGS_API_BASE

    @property
    def query_url(self) -> str:
        if self.site == "datadoghq.eu":
            return "https://api.datadoghq.eu/api/v2"
        return DATADOG_QUERY_API_BASE


class DatadogObservabilityClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or load_config()
        self.session = session or requests.Session()
        self.session.headers.update({
            "DD-API-KEY": self.config.dd_api_key,
            "DD-APPLICATION-KEY": self.config.dd_app_key,
            "Content-Type": "application/json",
        })

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        response = self.session.post(self.config.intake_url + "/logs", json={"ddsource": "app", **event.to_payload()})
        response.raise_for_status()
        return response.json() if response.content else {"status": "ok"}

    def write_logs(self, events):
        payload = [{"ddsource": "app", **event.to_payload()} for event in events]
        response = self.session.post(self.config.intake_url + "/logs", json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "ok"}

    def query_logs(self, query: LogQuery) -> LogQueryResult:
        params = query.to_dict()
        response = self.session.get(self.config.query_url + "/logs/events/search", params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("data", []) if isinstance(data, dict) else []
        return LogQueryResult.from_items(items, raw=data if isinstance(data, dict) else None)


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        dd_api_key=os.environ["DD_API_KEY"],
        dd_app_key=os.environ["DD_APP_KEY"],
        site=os.getenv("DD_SITE", "datadoghq.com"),
    )


def create_client() -> DatadogObservabilityClient:
    return DatadogObservabilityClient()
