from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import requests

from observability_models import MetricWindowRequest

DATADOG_API_HOST = "https://api.datadoghq.com"


@dataclass
class ObservabilityConfig:
    api_key: str
    app_key: str
    site: str = DATADOG_API_HOST

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        return cls(
            api_key=os.environ["DD_API_KEY"],
            app_key=os.environ["DD_APP_KEY"],
            site=os.getenv("DD_SITE", DATADOG_API_HOST),
        )


class DatadogMetricsClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None, session: Optional[requests.Session] = None) -> None:
        self.config = config or ObservabilityConfig.from_env()
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "DD-APPLICATION-KEY": self.config.app_key,
                "Content-Type": "application/json",
            }
        )

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.config.site}{path}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def query_metric_window(self, request: MetricWindowRequest) -> Dict[str, Any]:
        payload = request.to_payload()
        return self._get(
            "/api/v1/query",
            params={
                "from": payload["start_time"],
                "to": payload["end_time"],
                "query": request.metric_name,
                "statistics": ",".join(payload["statistics"]),
                "limit": payload["limit"],
                **({"resource_filter": payload["resource_filter"]} if "resource_filter" in payload else {}),
            },
        )

    def aggregate_metric_stats(self, request: MetricWindowRequest) -> Dict[str, Any]:
        payload = request.to_payload()
        return self._get(
            "/api/v1/series",
            params={
                "metric": request.metric_name,
                "from": payload["start_time"],
                "to": payload["end_time"],
                "rollup": "avg",
            },
        )

    def filter_metric_dimensions(self, request: MetricWindowRequest) -> Dict[str, Any]:
        payload = request.to_payload()
        return self._get(
            "/api/v1/query",
            params={
                "from": payload["start_time"],
                "to": payload["end_time"],
                "query": request.metric_name,
                "scope": ",".join(f"{k}:{v}" for k, v in (request.resource_filter or {}).items()),
            },
        )

    def compare_metric_series(self, left: MetricWindowRequest, right: MetricWindowRequest) -> Dict[str, Any]:
        return {
            "left": self.query_metric_window(left),
            "right": self.query_metric_window(right),
        }
