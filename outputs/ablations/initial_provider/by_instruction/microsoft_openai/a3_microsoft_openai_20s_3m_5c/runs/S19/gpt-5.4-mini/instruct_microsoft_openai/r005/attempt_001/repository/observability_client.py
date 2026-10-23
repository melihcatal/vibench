import os
from datetime import datetime
from typing import Any, Dict, Optional

import requests

from observability_models import MetricWindowRequest, MetricSeriesResponse


class ObservabilityClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("AZURE_MONITOR_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("AZURE_MONITOR_BASE_URL") or "https://management.azure.com"

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def query_metric_series(self, request: MetricWindowRequest, path: str = "/metrics/query") -> MetricSeriesResponse:
        response = requests.post(f"{self.base_url}{path}", json=request.to_dict(), headers=self._headers(), timeout=30)
        response.raise_for_status()
        return MetricSeriesResponse.from_dict(response.json())

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}{path}", params=params, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}{path}", json=payload, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()
