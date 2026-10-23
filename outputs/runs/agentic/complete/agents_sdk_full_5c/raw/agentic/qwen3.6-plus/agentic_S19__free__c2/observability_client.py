"""
Provide local configuration and client helper utilities for Managed Metrics Monitoring.

Provider: Datadog (datadog-api-client)
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v2.api.metrics_api import MetricsApi as MetricsApiV2


class ObservabilityClient:
    """Helper client wrapping Datadog API for metrics operations."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("DATADOG_API_KEY", "")
        self.app_key = app_key or os.environ.get("DATADOG_APP_KEY", "")
        self.site = site or os.environ.get("DATADOG_SITE", "datadoghq.com")

        if not self.api_key or not self.app_key:
            raise ValueError(
                "Datadog API credentials required. Set DATADOG_API_KEY and DATADOG_APP_KEY."
            )

        self._configuration = Configuration(
            api_key={
                "apiKeyAuth": self.api_key,
                "appKeyAuth": self.app_key,
            },
            host=f"https://api.{self.site}",
        )
        self._api_client = ApiClient(self._configuration)
        self.metrics_api = MetricsApi(self._api_client)
        self.metrics_api_v2 = MetricsApiV2(self._api_client)

    def get_api_client(self) -> ApiClient:
        """Return the underlying Datadog ApiClient."""
        return self._api_client

    def get_v1_api(self) -> MetricsApi:
        """Return Datadog v1 Metrics API client."""
        return self.metrics_api

    def get_v2_api(self) -> MetricsApiV2:
        """Return Datadog v2 Metrics API client."""
        return self.metrics_api_v2

    def build_query_context(
        self,
        metric_name: str,
        start: datetime,
        end: datetime,
        tags: Optional[Dict[str, str]] = None,
        aggregation: str = "avg",
    ) -> Dict[str, Any]:
        """Build a Datadog metric query context dict."""
        tag_parts = []
        if tags:
            tag_parts = [f"{k}:{v}" for k, v in tags.items()]
        query = f"{aggregation}:{metric_name}"
        if tag_parts:
            query += "{" + ",".join(tag_parts) + "}"
        return {
            "query": query,
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
        }

    def build_tags_list(self, tags: Optional[Dict[str, str]] = None) -> List[str]:
        """Convert tag dict to Datadog tag list format."""
        if not tags:
            return []
        return [f"{k}:{v}" for k, v in tags.items()]

    def close(self):
        """Close the underlying API client."""
        self._api_client.close()
