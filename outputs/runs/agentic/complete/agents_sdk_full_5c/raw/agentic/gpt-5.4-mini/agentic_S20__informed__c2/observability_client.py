from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from observability_models import IngestResponse, QueryRequest, QueryResponse, LogEvent

DATADOG_API_BASE = "https://api.datadoghq.com/api/v2"


@dataclass
class DatadogObservabilityClient:
    api_key: str
    app_key: str
    site: str = "datadoghq.com"
    timeout: float = 10.0

    @property
    def base_url(self) -> str:
        return f"https://api.{self.site}/api/v2"

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def ingest_log(self, event: LogEvent, index: Optional[str] = None) -> IngestResponse:
        payload: Dict[str, Any] = {"data": {"attributes": event.to_dict(), "type": "log"}}
        if index:
            payload["data"]["attributes"]["index"] = index
        response = requests.post(
            f"{self.base_url}/logs",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return IngestResponse(accepted=True, raw=response.json() if response.content else {})

    def query_logs(self, request: QueryRequest) -> QueryResponse:
        payload = {
            "filter": {
                "from": request.start_time,
                "to": request.end_time,
                "query": request.query,
            },
            "page": {"limit": request.limit},
        }
        response = requests.post(
            f"{self.base_url}/logs/events/search",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json() if response.content else {}
        entries = data.get("data", []) if isinstance(data, dict) else []
        return QueryResponse(entries=entries, raw=data if isinstance(data, dict) else {"data": data})


def load_client_from_env() -> DatadogObservabilityClient:
    api_key = os.environ["DD_API_KEY"]
    app_key = os.environ["DD_APP_KEY"]
    site = os.getenv("DD_SITE", "datadoghq.com")
    return DatadogObservabilityClient(api_key=api_key, app_key=app_key, site=site)
