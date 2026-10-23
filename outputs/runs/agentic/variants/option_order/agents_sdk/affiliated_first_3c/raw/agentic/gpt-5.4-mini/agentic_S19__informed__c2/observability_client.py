from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

DEFAULT_DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass(frozen=True)
class ObservabilityConfig:
    api_key: str
    app_key: str
    base_url: str = DEFAULT_DATADOG_API_BASE

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        api_key = os.environ.get("DD_API_KEY", "")
        app_key = os.environ.get("DD_APP_KEY", "")
        base_url = os.environ.get("DD_API_BASE_URL", DEFAULT_DATADOG_API_BASE)
        if not api_key or not app_key:
            raise RuntimeError("DD_API_KEY and DD_APP_KEY are required for Datadog Metrics API access")
        return cls(api_key=api_key, app_key=app_key, base_url=base_url.rstrip("/"))


class DatadogMetricsClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None) -> None:
        self.config = config or ObservabilityConfig.from_env()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "DD-APPLICATION-KEY": self.config.app_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.config.base_url}{path}"

    def query(self, query: str, start: datetime, end: datetime) -> Dict[str, Any]:
        params = {
            "query": query,
            "from": int(start.replace(tzinfo=timezone.utc).timestamp()),
            "to": int(end.replace(tzinfo=timezone.utc).timestamp()),
        }
        response = self.session.get(self._url("/api/v1/query"), params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def list_series(self, query: str, start: datetime, end: datetime) -> Dict[str, Any]:
        payload = {
            "from": int(start.replace(tzinfo=timezone.utc).timestamp()),
            "to": int(end.replace(tzinfo=timezone.utc).timestamp()),
            "query": query,
        }
        response = self.session.post(self._url("/api/v2/query/timeseries"), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_aggregate(self, metric_query: str, start: datetime, end: datetime, stats: Optional[list[str]] = None) -> Dict[str, Any]:
        payload = {
            "data": {
                "type": "timeseries_request",
                "attributes": {
                    "from": int(start.replace(tzinfo=timezone.utc).timestamp()),
                    "to": int(end.replace(tzinfo=timezone.utc).timestamp()),
                    "query": metric_query,
                    "compute": [{"aggregation": s, "interval": 60} for s in (stats or ["avg", "max", "min", "sum"])],
                },
            }
        }
        response = self.session.post(self._url("/api/v2/metrics/query"), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def archive_blob(self, container_url: str, path: str, content: bytes, content_type: str = "application/json") -> None:
        headers = {"x-ms-blob-type": "BlockBlob", "Content-Type": content_type}
        response = requests.put(f"{container_url.rstrip('/')}/{path.lstrip('/')}", data=content, headers=headers, timeout=30)
        response.raise_for_status()
