import os
from typing import Any, Dict, Optional

import requests


class ObservabilityClient:
    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_MONITOR_METRICS_ENDPOINT", "https://management.azure.com")
        self.api_key = api_key or os.getenv("AZURE_MONITOR_METRICS_API_KEY") or os.getenv("OPENAI_API_KEY")

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = self.endpoint.rstrip("/") + path
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
