import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class FilteredMetricPoint:
    timestamp: str
    value: float
    dimensions: Dict[str, Any]


class DatadogMetricDimensionFilterClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, site: Optional[str] = None):
        self.api_key = api_key or os.getenv("DATADOG_API_KEY")
        self.app_key = app_key or os.getenv("DATADOG_APP_KEY")
        self.site = site or os.getenv("DATADOG_SITE", "datadoghq.com")
        if not self.api_key or not self.app_key:
            raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    def filter_metric_dimensions(
        self,
        metric_name: str,
        dimensions: Optional[Dict[str, str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        interval: int = 60,
    ) -> List[FilteredMetricPoint]:
        end_time = end_time or datetime.now(timezone.utc)
        start_time = start_time or (end_time - timedelta(hours=1))
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        scope = self._build_scope(dimensions or {})
        query = f"avg:{metric_name}{{{scope}}}.rollup(avg,{interval})"
        url = f"https://api.{self.site}/api/v1/query"
        params = {
            "from": int(start_time.timestamp()),
            "to": int(end_time.timestamp()),
            "query": query,
        }
        headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return self._normalize_datadog_series(response.json())

    def _build_scope(self, dimensions: Dict[str, str]) -> str:
        if not dimensions:
            return "*"
        parts = []
        for key, value in sorted(dimensions.items()):
            if value is None:
                continue
            parts.append(f"{key}:{value}")
        return ",".join(parts) if parts else "*"

    def _normalize_datadog_series(self, payload: Dict[str, Any]) -> List[FilteredMetricPoint]:
        series = payload.get("series", [])
        points: List[FilteredMetricPoint] = []
        for item in series:
            scope = item.get("scope", "")
            dimensions = self._parse_scope(scope)
            for ts, value in item.get("pointlist", []):
                if value is None:
                    continue
                timestamp = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).isoformat()
                points.append(FilteredMetricPoint(timestamp=timestamp, value=float(value), dimensions=dimensions))
        return points

    def _parse_scope(self, scope: str) -> Dict[str, str]:
        dimensions: Dict[str, str] = {}
        if not scope:
            return dimensions
        for part in scope.split(","):
            if ":" not in part:
                continue
            key, value = part.split(":", 1)
            if key and value:
                dimensions[key] = value
        return dimensions


def filter_metric_dimensions(
    metric_name: str,
    dimensions: Optional[Dict[str, str]] = None,
    hours: int = 1,
    interval: int = 60,
) -> List[FilteredMetricPoint]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    client = DatadogMetricDimensionFilterClient()
    return client.filter_metric_dimensions(metric_name, dimensions=dimensions, start_time=start_time, end_time=end_time, interval=interval)
