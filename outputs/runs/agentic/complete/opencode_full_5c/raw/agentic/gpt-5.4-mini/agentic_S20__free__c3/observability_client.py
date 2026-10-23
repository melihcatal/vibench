import os
from typing import Any, Dict, Optional

import requests

from observability_models import LogEvent, LogQuery


class ManagedLogClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        source: Optional[str] = None,
    ):
        self.api_key = (
            api_key or os.getenv("SEQ_API_KEY") or os.getenv("DATADOG_API_KEY")
        )
        self.base_url = (
            base_url or os.getenv("SEQ_BASE_URL") or "https://example.logging.svc"
        )
        self.source = source or os.getenv("LOG_SOURCE", "python-service")

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json", "X-Log-Source": self.source}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def write_event(self, event: LogEvent) -> Dict[str, Any]:
        return requests.post(
            f"{self.base_url}/api/logs",
            json=event.to_payload(),
            headers=self._headers(),
            timeout=10,
        ).json()

    def query_logs(self, query: LogQuery) -> Dict[str, Any]:
        return requests.get(
            f"{self.base_url}/api/logs",
            params=query.to_filter(),
            headers=self._headers(),
            timeout=10,
        ).json()


def default_client() -> ManagedLogClient:
    return ManagedLogClient()
