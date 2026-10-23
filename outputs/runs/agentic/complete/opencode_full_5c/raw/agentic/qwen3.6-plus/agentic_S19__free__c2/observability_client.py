from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

import httpx

DATADOG_API_URL = "https://api.datadoghq.com"
DATADOG_API_V1_PREFIX = "/api/v1"
DATADOG_API_V2_PREFIX = "/api/v2"

ENV_DD_API_KEY = "DD_API_KEY"
ENV_DD_APP_KEY = "DD_APP_KEY"
ENV_DD_SITE = "DD_SITE"


class DatadogConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get(ENV_DD_API_KEY, "")
        self.app_key = app_key or os.environ.get(ENV_DD_APP_KEY, "")
        site_val = site or os.environ.get(ENV_DD_SITE, "datadoghq.com")
        self.api_url = f"https://api.{site_val}"
        self.api_v1_url = f"{self.api_url}{DATADOG_API_V1_PREFIX}"
        self.api_v2_url = f"{self.api_url}{DATADOG_API_V2_PREFIX}"

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError(
                f"Datadog API key is required. Set {ENV_DD_API_KEY} environment variable."
            )
        if not self.app_key:
            raise ValueError(
                f"Datadog Application key is required. Set {ENV_DD_APP_KEY} environment variable."
            )


class ObservabilityClient:
    def __init__(self, config: Optional[DatadogConfig] = None):
        self.config = config or DatadogConfig()
        self.config.validate()
        self._http_client: Optional[httpx.Client] = None

    @property
    def http_client(self) -> httpx.Client:
        if self._http_client is None:
            self._http_client = httpx.Client(
                base_url=self.config.api_url,
                timeout=httpx.Timeout(30.0, connect=10.0),
                headers=self._default_headers(),
            )
        return self._http_client

    def _default_headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.config.api_key,
            "DD-APPLICATION-KEY": self.config.app_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_v1_url(self, path: str) -> str:
        return f"{self.config.api_v1_url}{path}"

    def get_v2_url(self, path: str) -> str:
        return f"{self.config.api_v2_url}{path}"

    def request_v1(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        url = self.get_v1_url(path)
        return self.http_client.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            headers=self._default_headers(),
        )

    def request_v2(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        url = self.get_v2_url(path)
        return self.http_client.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            headers=self._default_headers(),
        )

    def query_metrics_v1(
        self,
        query: str,
        start: int,
        end: int,
        interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "from": start,
            "to": end,
            "query": query,
        }
        if interval is not None:
            params["interval"] = interval
        response = self.request_v1("GET", "/query", params=params)
        response.raise_for_status()
        return response.json()

    def query_metrics_v2(
        self,
        queries: List[Dict[str, Any]],
        from_ts: int,
        to_ts: int,
        formula: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "data": {
                "attributes": {
                    "queries": queries,
                    "from": from_ts,
                    "to": to_ts,
                }
            }
        }
        if formula:
            body["data"]["attributes"]["formulas"] = [{"formula": formula}]
        response = self.request_v2("POST", "/query/timeseries", json_body=body)
        response.raise_for_status()
        return response.json()

    def get_metric_metadata(self, metric_name: str) -> Dict[str, Any]:
        response = self.request_v1("GET", f"/metrics/{metric_name}")
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        if self._http_client is not None:
            self._http_client.close()
            self._http_client = None

    def __enter__(self) -> "ObservabilityClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


def create_client(
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: Optional[str] = None,
) -> ObservabilityClient:
    config = DatadogConfig(api_key=api_key, app_key=app_key, site=site)
    return ObservabilityClient(config=config)
