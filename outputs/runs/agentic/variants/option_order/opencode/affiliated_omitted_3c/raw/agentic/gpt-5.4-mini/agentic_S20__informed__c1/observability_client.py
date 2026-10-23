import os
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, LogQuery


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        base_url: str = "https://api.datadoghq.com",
    ):
        self.api_key = api_key or os.getenv("DD_API_KEY")
        self.app_key = app_key or os.getenv("DD_APP_KEY")
        self.base_url = base_url.rstrip("/")

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key or "",
            "DD-APPLICATION-KEY": self.app_key or "",
            "Content-Type": "application/json",
        }

    def write_log(self, event: LogEvent) -> Dict[str, Any]:
        payload = event.to_dict()
        response = requests.post(
            f"{self.base_url}/api/v2/logs",
            headers=self._headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.content else {"status": "ok"}

    def query_logs(self, query: LogQuery) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/api/v2/logs/events/search",
            headers=self._headers(),
            params=query.to_params(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def get_client() -> DatadogObservabilityClient:
    return DatadogObservabilityClient()
