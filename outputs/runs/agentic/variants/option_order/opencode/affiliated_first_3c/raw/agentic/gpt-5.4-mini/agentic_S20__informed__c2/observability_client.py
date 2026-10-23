import os
from typing import Any, Dict, List, Optional

import requests

from observability_models import LogQuery


class DatadogLogsClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("DD_API_KEY", "")
        self.app_key = app_key or os.getenv("DD_APP_KEY", "")
        self.site = site or os.getenv("DD_SITE", "datadoghq.com")
        self.base_url = f"https://api.{self.site}/api/v2/logs"

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def write_log(self, record: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            self.base_url,
            headers=self._headers(),
            json={"data": [{"attributes": record}]},
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.content else {}

    def query_logs(self, query: LogQuery) -> Dict[str, Any]:
        payload = {
            "filter": {
                "query": query.query,
                "from": query.start_time,
                "to": query.end_time,
            },
            "page": {"limit": 100},
        }
        response = requests.post(
            f"https://api.{self.site}/api/v2/logs/events/search",
            headers=self._headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
