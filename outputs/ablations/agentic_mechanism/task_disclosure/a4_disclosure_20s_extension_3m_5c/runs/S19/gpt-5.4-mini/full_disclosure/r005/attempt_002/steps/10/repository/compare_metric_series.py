import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class SeriesPoint:
    timestamp: str
    value: float


@dataclass
class SeriesComparison:
    left_resource: str
    right_resource: str
    window_start: str
    window_end: str
    left_points: List[SeriesPoint]
    right_points: List[SeriesPoint]
    difference: float
    ratio: Optional[float]


class DatadogMetricSeriesClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, site: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DATADOG_API_KEY")
        self.app_key = app_key or os.environ.get("DATADOG_APP_KEY")
        self.site = site or os.environ.get("DATADOG_SITE", "datadoghq.com")
        if not self.api_key or not self.app_key:
            raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    @property
    def base_url(self) -> str:
        return f"https://api.{self.site}"

    def compare_metric_series(
        self,
        metric_name: str,
        left_filter: str,
        right_filter: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval_seconds: int = 60,
    ) -> SeriesComparison:
        end = end or datetime.now(timezone.utc)
        start = start or (end - timedelta(hours=1))
        params_left = {
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
            "query": f"avg:{metric_name}{{{left_filter}}}.rollup(avg,{interval_seconds})",
        }
        params_right = {
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
            "query": f"avg:{metric_name}{{{right_filter}}}.rollup(avg,{interval_seconds})",
        }
        left_series = self._fetch_series(params_left)
        right_series = self._fetch_series(params_right)
        left_total = sum(p.value for p in left_series)
        right_total = sum(p.value for p in right_series)
        difference = left_total - right_total
        ratio = (left_total / right_total) if right_total not in (0, 0.0) else None
        return SeriesComparison(
            left_resource=left_filter,
            right_resource=right_filter,
            window_start=start.isoformat(),
            window_end=end.isoformat(),
            left_points=left_series,
            right_points=right_series,
            difference=difference,
            ratio=ratio,
        )

    def _fetch_series(self, params: Dict[str, Any]) -> List[SeriesPoint]:
        response = requests.get(
            f"{self.base_url}/api/v1/query",
            headers={
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key,
            },
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        series = payload.get("series", [])
        points: List[SeriesPoint] = []
        for item in series:
            for ts, value in item.get("pointlist", []):
                if ts is None or value is None:
                    continue
                points.append(SeriesPoint(timestamp=datetime.fromtimestamp(ts / 1000, tz=timezone.utc).isoformat(), value=float(value)))
        return points


def compare_metric_series(metric_name: str, left_filter: str, right_filter: str) -> Dict[str, Any]:
    client = DatadogMetricSeriesClient()
    result = client.compare_metric_series(metric_name=metric_name, left_filter=left_filter, right_filter=right_filter)
    return {
        "left_resource": result.left_resource,
        "right_resource": result.right_resource,
        "window_start": result.window_start,
        "window_end": result.window_end,
        "left_points": [point.__dict__ for point in result.left_points],
        "right_points": [point.__dict__ for point in result.right_points],
        "difference": result.difference,
        "ratio": result.ratio,
    }
