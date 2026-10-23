import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class MetricStats:
    count: int
    sum: float
    average: float
    minimum: float
    maximum: float


class DatadogMetricStatsClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, site: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DATADOG_API_KEY")
        self.app_key = app_key or os.environ.get("DATADOG_APP_KEY")
        self.site = site or os.environ.get("DATADOG_SITE", "datadoghq.com")
        if not self.api_key or not self.app_key:
            raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    def aggregate_metric_stats(self, metric_name: str, start_ts: int, end_ts: int, interval: int = 300, aggregator: str = "avg") -> MetricStats:
        url = f"https://api.{self.site}/api/v1/query"
        params = {
            "from": start_ts,
            "to": end_ts,
            "query": f"{aggregator}:{metric_name}{{*}}.rollup({interval})",
        }
        headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        payload: Dict[str, Any] = response.json()
        series = payload.get("series", [])
        values = []
        for item in series:
            values.extend(v for v in item.get("pointlist", []) if v[1] is not None)
        numeric_values = [float(v[1]) for v in values]
        if not numeric_values:
            return MetricStats(count=0, sum=0.0, average=0.0, minimum=0.0, maximum=0.0)
        total = sum(numeric_values)
        return MetricStats(
            count=len(numeric_values),
            sum=total,
            average=total / len(numeric_values),
            minimum=min(numeric_values),
            maximum=max(numeric_values),
        )


def aggregate_metric_stats(metric_name: str, window_seconds: int, interval: int = 300, aggregator: str = "avg") -> MetricStats:
    end_ts = int(time.time())
    start_ts = end_ts - window_seconds
    client = DatadogMetricStatsClient()
    return client.aggregate_metric_stats(metric_name, start_ts, end_ts, interval=interval, aggregator=aggregator)
