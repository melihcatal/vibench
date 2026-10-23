import os
from typing import Any, Dict, Optional

import requests


class DatadogObservabilityClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("DD_API_KEY", "")
        self.app_key = app_key or os.getenv("DD_APP_KEY", "")
        self.site = site or os.getenv("DD_SITE", "datadoghq.com")
        self.base_url = f"https://api.{self.site}/api/v1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key,
                "Content-Type": "application/json",
            }
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def query_metrics(self, query: str, start: int, end: int) -> Dict[str, Any]:
        return self.get("/query", params={"query": query, "from": start, "to": end})


def get_client() -> DatadogObservabilityClient:
    return DatadogObservabilityClient()
