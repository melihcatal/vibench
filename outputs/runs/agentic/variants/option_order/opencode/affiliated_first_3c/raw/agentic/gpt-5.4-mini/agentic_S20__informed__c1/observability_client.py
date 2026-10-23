import os
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests

from observability_models import LogEvent, normalize_fields


DD_API_BASE = os.getenv("DD_API_BASE", "https://api.datadoghq.com/api/v2")


def load_observability_config() -> Dict[str, str]:
    return {
        "api_key": os.environ["DD_API_KEY"],
        "app_key": os.environ["DD_APP_KEY"],
        "site": os.getenv("DD_SITE", "datadoghq.com"),
        "base_url": os.getenv("DD_API_BASE", DD_API_BASE),
    }


class DatadogLogsClient:
    def __init__(self, api_key: str, app_key: str, base_url: str = DD_API_BASE):
        self.api_key = api_key
        self.app_key = app_key
        self.base_url = base_url.rstrip("/")

    @classmethod
    def from_env(cls) -> "DatadogLogsClient":
        cfg = load_observability_config()
        return cls(cfg["api_key"], cfg["app_key"], cfg["base_url"])

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def write_event(self, event: Mapping[str, Any]) -> Dict[str, Any]:
        payload = {"data": {"attributes": dict(event)}}
        response = requests.post(
            f"{self.base_url}/logs", headers=self._headers(), json=payload, timeout=30
        )
        response.raise_for_status()
        return response.json() if response.content else {"status": response.status_code}

    def write_events(self, events: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
        return [self.write_event(event) for event in events]

    def query_logs(
        self, query: str, start_time: str, end_time: str, limit: int = 50
    ) -> Dict[str, Any]:
        payload = {
            "filter": {"from": start_time, "to": end_time, "query": query},
            "page": {"limit": limit},
            "sort": "-timestamp",
        }
        response = requests.post(
            f"{self.base_url}/logs/events/search",
            headers=self._headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def build_log_event(
    message: Any, severity: str = "INFO", fields: Optional[Mapping[str, Any]] = None
) -> Dict[str, Any]:
    return LogEvent.create(
        message=message, severity=severity, fields=normalize_fields(fields)
    ).to_dict()
