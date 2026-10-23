import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ManagedMetricsMonitoringConfig:
    base_url: str
    api_key: str
    timeout_seconds: float = 30.0


def load_managed_metrics_monitoring_config() -> ManagedMetricsMonitoringConfig:
    base_url = os.getenv("DATADOG_API_BASE_URL", "https://api.datadoghq.com")
    api_key = os.getenv("DATADOG_API_KEY", "")
    timeout_seconds = float(os.getenv("DATADOG_TIMEOUT_SECONDS", "30"))
    if not api_key:
        raise ValueError("DATADOG_API_KEY is required")
    return ManagedMetricsMonitoringConfig(base_url=base_url.rstrip("/"), api_key=api_key, timeout_seconds=timeout_seconds)


class ManagedMetricsMonitoringClient:
    def __init__(self, config: Optional[ManagedMetricsMonitoringConfig] = None) -> None:
        self.config = config or load_managed_metrics_monitoring_config()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def get_metric_summary(self, metric_name: str, from_ts: int, to_ts: int) -> Dict[str, Any]:
        url = f"{self.config.base_url}/api/v1/query"
        response = self._session.get(
            url,
            params={"from": from_ts, "to": to_ts, "query": metric_name},
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def list_monitors(self) -> Dict[str, Any]:
        url = f"{self.config.base_url}/api/v1/monitor"
        response = self._session.get(url, timeout=self.config.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self._session.close()
