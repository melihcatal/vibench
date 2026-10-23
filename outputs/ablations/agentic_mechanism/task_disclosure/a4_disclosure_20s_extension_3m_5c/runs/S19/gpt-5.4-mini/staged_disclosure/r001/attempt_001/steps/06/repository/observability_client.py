import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class ManagedMetricsMonitoringConfig:
    api_key: str
    base_url: str = "https://api.datadoghq.com"
    site: str = "datadoghq.com"
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "ManagedMetricsMonitoringConfig":
        api_key = os.getenv("DATADOG_API_KEY") or os.getenv("DD_API_KEY")
        if not api_key:
            raise ValueError("Missing Datadog API key in DATADOG_API_KEY or DD_API_KEY")
        base_url = os.getenv("DATADOG_API_URL", "https://api.datadoghq.com")
        site = os.getenv("DATADOG_SITE", "datadoghq.com")
        timeout = float(os.getenv("DATADOG_TIMEOUT_SECONDS", "30"))
        return cls(api_key=api_key, base_url=base_url.rstrip("/"), site=site, timeout=timeout)


class ManagedMetricsMonitoringClient:
    def __init__(self, config: Optional[ManagedMetricsMonitoringConfig] = None):
        self.config = config or ManagedMetricsMonitoringConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kwargs):
        url = f"{self.config.base_url}{path}"
        response = self._session.request(method, url, timeout=self.config.timeout, **kwargs)
        response.raise_for_status()
        if response.content:
            return response.json()
        return None

    def get_metric_metadata(self, metric_name: str):
        return self._request("GET", f"/api/v1/metrics/{metric_name}")

    def query_metrics(self, query: str, from_ts: int, to_ts: int):
        params = {"query": query, "from": from_ts, "to": to_ts}
        return self._request("GET", "/api/v1/query", params=params)

    def list_active_metrics(self):
        return self._request("GET", "/api/v1/metrics")
