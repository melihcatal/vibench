from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import os

import requests

from observability_models import (
    LogEvent,
    LogQueryRequest,
    LogQueryResponse,
    parse_datadog_search_response,
)


@dataclass(slots=True)
class DatadogConfig:
    api_key: str
    app_key: str
    site: str
    hostname: str

    @property
    def logs_intake_url(self) -> str:
        return f"https://http-intake.logs.{self.site}/api/v2/logs"

    @property
    def logs_search_url(self) -> str:
        return f"https://api.{self.site}/api/v2/logs/events/search"


def load_datadog_config() -> DatadogConfig:
    return DatadogConfig(
        api_key=os.environ["DATADOG_API_KEY"],
        app_key=os.environ["DATADOG_APP_KEY"],
        site=os.getenv("DATADOG_SITE", "datadoghq.com"),
        hostname=os.getenv("DATADOG_HOSTNAME", "python-service"),
    )


class DatadogObservabilityClient:
    def __init__(
        self, config: DatadogConfig | None = None, timeout: float = 15.0
    ) -> None:
        self.config = config or load_datadog_config()
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "Content-Type": "application/json",
            }
        )

    def write_logs(self, events: list[LogEvent]) -> dict[str, Any]:
        payload = [event.to_datadog_payload(self.config.hostname) for event in events]
        response = self.session.post(
            self.config.logs_intake_url, json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        return {"status_code": response.status_code, "submitted": len(payload)}

    def search_logs(self, request: LogQueryRequest) -> LogQueryResponse:
        headers = {"DD-APPLICATION-KEY": self.config.app_key}
        payload = {
            "filter": {
                "query": request.query,
                "from": request.from_time,
                "to": request.to_time,
            },
            "page": {"limit": request.limit},
            "sort": request.sort,
        }
        response = self.session.post(
            self.config.logs_search_url,
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return parse_datadog_search_response(response.json())
