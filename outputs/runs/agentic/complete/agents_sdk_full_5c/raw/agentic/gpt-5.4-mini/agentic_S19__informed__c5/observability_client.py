from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

DATADOG_API_HOST = "https://api.datadoghq.com"


@dataclass(slots=True)
class ObservabilityConfig:
    api_key: str
    app_key: str
    site: str = DATADOG_API_HOST
    timeout: int = 30

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        return cls(
            api_key=os.environ.get("DD_API_KEY", ""),
            app_key=os.environ.get("DD_APP_KEY", ""),
            site=os.environ.get("DD_SITE", DATADOG_API_HOST),
        )


class DatadogMetricsClient:
    def __init__(self, config: ObservabilityConfig | None = None) -> None:
        self.config = config or ObservabilityConfig.from_env()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "DD-API-KEY": self.config.api_key,
                "DD-APPLICATION-KEY": self.config.app_key,
                "Content-Type": "application/json",
            }
        )

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        response = self.session.get(f"{self.config.site}{path}", params=params, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()

    def query_series(self, metric_name: str, start: str, end: str, dimensions: dict[str, str] | None = None, aggregation: str = "avg") -> dict[str, Any]:
        params = {
            "from": start,
            "to": end,
            "query": f"{aggregation}:{metric_name}{{*}}",
        }
        if dimensions:
            dim_filter = ",".join(f"{k}:{v}" for k, v in dimensions.items())
            params["query"] = f"{aggregation}:{metric_name}{{{dim_filter}}}"
        return self._get("/api/v1/query", params=params)

    def get_aggregates(self, metric_name: str, start: str, end: str, rollup: int = 60) -> dict[str, Any]:
        params = {"from": start, "to": end, "query": f"{metric_name}.rollup({rollup})"}
        return self._get("/api/v1/query", params=params)

    def export_snapshot(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{self.config.site}/api/v1/series", json=payload, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()
