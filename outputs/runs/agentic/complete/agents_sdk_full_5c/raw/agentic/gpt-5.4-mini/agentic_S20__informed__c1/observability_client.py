from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, normalize_log_event


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_key: str
    site: str = "datadoghq.com"

    @property
    def base_url(self) -> str:
        return f"https://api.{self.site}"


class DatadogLogsClient:
    def __init__(self, config: DatadogConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": config.api_key,
                "DD-APPLICATION-KEY": config.app_key,
                "Content-Type": "application/json",
            }
        )

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        payload = normalize_log_event(event)
        response = self.session.post(
            f"{self.config.base_url}/api/v2/logs",
            json=[payload],
            timeout=30,
        )
        response.raise_for_status()
        return {"status_code": response.status_code, "payload": payload}

    def query_logs(self, query: str, start: datetime, end: datetime, limit: int = 100) -> Dict[str, Any]:
        params = {
            "filter[query]": query,
            "filter[from]": _iso_z(start),
            "filter[to]": _iso_z(end),
            "page[limit]": limit,
        }
        response = self.session.get(
            f"{self.config.base_url}/api/v2/logs/events/search",
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def load_config() -> DatadogConfig:
    return DatadogConfig(
        api_key=os.environ["DD_API_KEY"],
        app_key=os.environ["DD_APP_KEY"],
        site=os.getenv("DD_SITE", "datadoghq.com"),
    )


def build_client() -> DatadogLogsClient:
    return DatadogLogsClient(load_config())


def _iso_z(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
