import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class ManagedMetricsMonitoringConfig:
    project_id: str
    location: str
    metrics_scope: Optional[str] = None
    api_key: Optional[str] = None
    base_url: str = "https://monitoring.googleapis.com/v3"

    @classmethod
    def from_env(cls) -> "ManagedMetricsMonitoringConfig":
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
        location = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("GCP_LOCATION") or "global"
        metrics_scope = os.environ.get("GOOGLE_CLOUD_METRICS_SCOPE")
        api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
        base_url = os.environ.get("GOOGLE_CLOUD_MONITORING_BASE_URL", cls.base_url)
        return cls(
            project_id=project_id,
            location=location,
            metrics_scope=metrics_scope,
            api_key=api_key,
            base_url=base_url,
        )


class ManagedMetricsMonitoringClient:
    def __init__(self, config: Optional[ManagedMetricsMonitoringConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or ManagedMetricsMonitoringConfig.from_env()
        self.session = session or requests.Session()

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        headers = {"Accept": "application/json"}
        if self.config.api_key:
            params = dict(params or {})
            params["key"] = self.config.api_key
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = self.session.request(method, url, headers=headers, params=params, json=json, timeout=30)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def list_metric_descriptors(self) -> Dict[str, Any]:
        if not self.config.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
        path = f"projects/{self.config.project_id}/metricDescriptors"
        return self._request("GET", path)

    def list_time_series(self, filter_expression: str, interval: Optional[Dict[str, Any]] = None, aggregation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.config.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
        path = f"projects/{self.config.project_id}/timeSeries"
        payload: Dict[str, Any] = {"filter": filter_expression}
        if interval:
            payload["interval"] = interval
        if aggregation:
            payload["aggregation"] = aggregation
        return self._request("GET", path, params=payload)

    def create_alert_policy(self, alert_policy: Dict[str, Any]) -> Dict[str, Any]:
        if not self.config.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
        path = f"projects/{self.config.project_id}/alertPolicies"
        return self._request("POST", path, json=alert_policy)


def build_managed_metrics_client() -> ManagedMetricsMonitoringClient:
    return ManagedMetricsMonitoringClient()
