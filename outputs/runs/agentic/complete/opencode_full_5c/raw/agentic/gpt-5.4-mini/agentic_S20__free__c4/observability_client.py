import os
from typing import Any, Dict

import requests

from observability_models import LogIngestionRequest, LogQueryRequest


class ObservabilityClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.environ.get("NEW_RELIC_API_KEY", "")
        self.base_url = base_url or os.environ.get(
            "NEW_RELIC_API_BASE_URL", "https://api.newrelic.com"
        )

    def _headers(self) -> Dict[str, str]:
        return {
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def write_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        request = LogIngestionRequest(event)
        response = requests.post(
            f"{self.base_url}/v1/logs",
            json=request.to_payload(),
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def query_logs(self, query: LogQueryRequest) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/v1/logs/query",
            json=query.to_payload(),
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
