from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

from observability_models import MetricWindowRequest

DD_API_HOST = "https://api.datadoghq.com"
DD_METRICS_HOST = "api.datadoghq.com"


@dataclass(slots=True)
class ObservabilityConfig:
    dd_api_key: str
    dd_app_key: str
    base_url: str = DD_API_HOST


class DatadogMetricsClient:
    def __init__(self, config: Optional[ObservabilityConfig] = None, session: Optional[requests.Session] = None) -> None:
        self.config = config or load_config()
        self.session = session or requests.Session()

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.config.dd_api_key,
            "DD-APPLICATION-KEY": self.config.dd_app_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def query_series(self, request: MetricWindowRequest) -> Dict[str, Any]:
        req = request.normalized()
        params = {
            "from": int(req.start_time.timestamp()),
            "to": int(req.end_time.timestamp()),
            "query": self._build_query(req),
        }
        response = self.session.get(f"{self.config.base_url}/api/v1/query", headers=self._headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def aggregate_stats(self, request: MetricWindowRequest) -> Dict[str, Any]:
        payload = {
            "data": {
                "type": "timeseries_request",
                "attributes": {
                    "from": request.normalized().start_time.isoformat(),
                    "to": request.normalized().end_time.isoformat(),
                    "queries": [
                        {
                            "data_source": "metrics",
                            "name": request.metric_name,
                            "query": self._build_query(request.normalized()),
                        }
                    ],
                },
            }
        }
        response = self.session.post(f"{self.config.base_url}/api/v2/metrics/query", headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def _build_query(self, request: MetricWindowRequest) -> str:
        filters = []
        if request.resource:
            filters.append(f"host:{request.resource}")
        filters.extend(f"{k}:{v}" for k, v in request.dimensions.items())
        filter_clause = "{" + ",".join(filters) + "}" if filters else ""
        return f"{request.aggregation}:{request.metric_name}{filter_clause}"


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        dd_api_key=os.environ["DD_API_KEY"],
        dd_app_key=os.environ["DD_APP_KEY"],
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
