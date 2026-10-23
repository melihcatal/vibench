from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, LogQuery, LogResponse, ensure_iso8601

DATADOG_API_HOST = "https://api.datadoghq.com"
DATADOG_LOGS_QUERY_PATH = "/api/v2/logs/events/search"
DATADOG_LOGS_INGEST_PATH = "/api/v1/input"


@dataclass
class ObservabilityConfig:
    dd_api_key: str
    dd_app_key: str
    dd_site: str = DATADOG_API_HOST

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        return cls(
            dd_api_key=os.environ["DD_API_KEY"],
            dd_app_key=os.environ["DD_APP_KEY"],
            dd_site=os.getenv("DD_SITE", DATADOG_API_HOST),
        )


class DatadogLogsClient:
    def __init__(self, config: ObservabilityConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": config.dd_api_key,
                "DD-APPLICATION-KEY": config.dd_app_key,
                "Content-Type": "application/json",
            }
        )

    def write_event(self, event: LogEvent) -> Dict[str, Any]:
        payload = event.to_dict()
        response = self.session.post(
            f"{self.config.dd_site}{DATADOG_LOGS_INGEST_PATH}",
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        return {"accepted": True, "status_code": response.status_code, "payload": payload}

    def query_logs(self, query: LogQuery) -> LogResponse:
        payload: Dict[str, Any] = {
            "filter": {"query": query.to_datadog_query(), "limit": query.limit},
        }
        if query.start_time:
            payload["filter"]["from"] = ensure_iso8601(query.start_time)
        if query.end_time:
            payload["filter"]["to"] = ensure_iso8601(query.end_time)
        response = self.session.post(
            f"{self.config.dd_site}{DATADOG_LOGS_QUERY_PATH}",
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        return LogResponse.from_datadog(response.json())


def build_client_from_env() -> DatadogLogsClient:
    return DatadogLogsClient(ObservabilityConfig.from_env())


def time_range(minutes: int = 15) -> tuple[str, str]:
    end = datetime.now(timezone.utc)
    start = end - __import__("datetime").timedelta(minutes=minutes)
    return ensure_iso8601(start), ensure_iso8601(end)
