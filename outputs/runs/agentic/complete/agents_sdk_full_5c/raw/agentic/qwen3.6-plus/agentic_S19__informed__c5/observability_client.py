"""
observability_client.py - Local configuration and client helper utilities
for Managed Metrics Monitoring using Datadog Metrics API.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests

from observability_models import (
    MetricQueryRequest,
    MetricQueryResponse,
    build_metric_series_from_datadog,
    compute_series_stats,
    MetricSeries,
    MetricStats,
    time_window_to_epoch_minutes,
)


class DatadogConfig:
    """Datadog API configuration loaded from environment variables."""

    DEFAULT_API_URL = "https://api.datadoghq.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        api_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("DD_API_KEY", "")
        self.app_key = app_key or os.environ.get("DD_APP_KEY", "")
        self.api_url = api_url or os.environ.get(
            "DD_SITE_URL", self.DEFAULT_API_URL
        )

        if not self.api_key:
            raise ValueError("DD_API_KEY environment variable is required")
        if not self.app_key:
            raise ValueError("DD_APP_KEY environment variable is required")

    @property
    def query_url(self) -> str:
        return urljoin(self.api_url, "/api/v1/query")

    @property
    def query_v1_url(self) -> str:
        return urljoin(self.api_url, "/api/v1/query")

    def headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }


class DatadogMetricsClient:
    """Client wrapper for Datadog Metrics API v1 query endpoint."""

    def __init__(self, config: Optional[DatadogConfig] = None):
        self.config = config or DatadogConfig()
        self.session = requests.Session()
        self.session.headers.update(self.config.headers())

    def query(self, request: MetricQueryRequest) -> MetricQueryResponse:
        """Execute a metric query against Datadog and return normalized response."""
        payload = request.to_dict()
        params: Dict[str, Any] = {
            "from": request.from_ts,
            "to": request.to_ts,
            "query": request.metric_name,
        }
        if request.aggregation:
            params["aggregator"] = request.aggregation
        if request.rollup:
            params["rollup"] = request.rollup
        if request.tags:
            params["tags"] = ",".join(request.tags)

        response = self.session.get(
            self.config.query_v1_url, params=params, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        series_list: List[MetricSeries] = []
        for raw_series in data.get("series", []):
            series_list.append(build_metric_series_from_datadog(raw_series))

        return MetricQueryResponse(
            series=series_list,
            query=request.metric_name,
            from_ts=request.from_ts,
            to_ts=request.to_ts,
            resolution=data.get("resp_version"),
            status=data.get("status", "ok"),
        )

    def query_with_tags(
        self, metric_name: str, tags: List[str], from_ts: int, to_ts: int
    ) -> MetricQueryResponse:
        """Convenience method to query metric data filtered by tags/dimensions."""
        request = MetricQueryRequest(
            metric_name=metric_name,
            from_ts=from_ts,
            to_ts=to_ts,
            tags=tags,
        )
        return self.query(request)


def build_windowed_request(
    metric_name: str,
    window_minutes: int = 60,
    to_ts: Optional[int] = None,
    aggregation: Optional[str] = None,
    rollup: Optional[int] = None,
    tags: Optional[List[str]] = None,
) -> MetricQueryRequest:
    """Build a MetricQueryRequest for a given time window in minutes."""
    from_ts, to_ts = time_window_to_epoch_minutes(window_minutes, to_ts)
    return MetricQueryRequest(
        metric_name=metric_name,
        from_ts=from_ts,
        to_ts=to_ts,
        aggregation=aggregation,
        rollup=rollup,
        tags=tags,
    )


def build_tagged_request(
    metric_name: str,
    tags: List[str],
    window_minutes: int = 60,
    to_ts: Optional[int] = None,
) -> MetricQueryRequest:
    """Build a MetricQueryRequest filtered by resource tags."""
    from_ts, to_ts = time_window_to_epoch_minutes(window_minutes, to_ts)
    return MetricQueryRequest(
        metric_name=metric_name,
        from_ts=from_ts,
        to_ts=to_ts,
        tags=tags,
    )
