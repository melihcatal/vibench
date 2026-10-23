import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class ManagedMetricsConfig:
    api_key: str
    project_id: str
    base_url: str = "https://api.datadoghq.com"
    site: str = "datadoghq.com"


def load_managed_metrics_config() -> ManagedMetricsConfig:
    api_key = os.getenv("DATADOG_API_KEY", "").strip()
    project_id = os.getenv("DATADOG_PROJECT_ID", "").strip()
    base_url = os.getenv("DATADOG_API_BASE_URL", "https://api.datadoghq.com").strip()
    site = os.getenv("DATADOG_SITE", "datadoghq.com").strip()
    if not api_key:
        raise ValueError("DATADOG_API_KEY is required")
    if not project_id:
        raise ValueError("DATADOG_PROJECT_ID is required")
    return ManagedMetricsConfig(api_key=api_key, project_id=project_id, base_url=base_url, site=site)


class ManagedMetricsClient:
    def __init__(self, config: Optional[ManagedMetricsConfig] = None) -> None:
        self.config = config or load_managed_metrics_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def list_monitors(self, page: int = 0, per_page: int = 100):
        url = f"{self.config.base_url}/api/v1/monitor"
        response = self.session.get(url, params={"page": page, "per_page": per_page}, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_monitor(self, monitor_id: int):
        url = f"{self.config.base_url}/api/v1/monitor/{monitor_id}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def query_metrics(self, query: str, from_ts: int, to_ts: int):
        url = f"{self.config.base_url}/api/v1/query"
        response = self.session.get(
            url,
            params={"from": from_ts, "to": to_ts, "query": query},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
