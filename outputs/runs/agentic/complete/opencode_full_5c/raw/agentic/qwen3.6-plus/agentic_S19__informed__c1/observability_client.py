from __future__ import annotations

import os
from typing import Any

import requests


DATADOG_API_BASE = os.environ.get("DD_API_BASE", "https://api.datadoghq.com/api/v1")
DATADOG_SITE = os.environ.get("DD_SITE", "datadoghq.com")


class DatadogConfig:
    def __init__(
        self,
        api_key: str | None = None,
        app_key: str | None = None,
        api_base: str | None = None,
    ):
        self.api_key = api_key or os.environ.get("DD_API_KEY", "")
        self.app_key = app_key or os.environ.get("DD_APP_KEY", "")
        self.api_base = api_base or DATADOG_API_BASE
        if not self.api_key or not self.app_key:
            raise ValueError(
                "DD_API_KEY and DD_APP_KEY environment variables must be set"
            )

    def auth_headers(self) -> dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }


class DatadogClient:
    def __init__(self, config: DatadogConfig | None = None):
        self.config = config or DatadogConfig()
        self.session = requests.Session()
        self.session.headers.update(self.config.auth_headers())
        self.session.timeout = 30

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.config.api_base}{path}"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.config.api_base}{path}"
        resp = self.session.post(url, json=json)
        resp.raise_for_status()
        return resp.json()

    def query_metrics(self, query: str, start_ts: int, end_ts: int) -> dict[str, Any]:
        return self.get(
            "/query", params={"query": query, "from": start_ts, "to": end_ts}
        )

    def query_metrics_post(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.post("/query", json=payload)

    def check_health(self) -> bool:
        try:
            resp = self.session.get(f"{self.config.api_base}/validate-keys")
            return resp.status_code == 200
        except requests.RequestException:
            return False


def build_metric_query_string(
    metric: str, aggregator: str = "avg", dimensions: dict[str, str] | None = None
) -> str:
    dim_parts = []
    if dimensions:
        dim_parts = [f"{k}:{v}" for k, v in dimensions.items()]
    base = f"{aggregator}:{metric}"
    if dim_parts:
        base += "{" + ",".join(dim_parts) + "}"
    return base
