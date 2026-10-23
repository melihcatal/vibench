import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class MetricDatapoint:
    timestamp: str
    value: float
    dimensions: Dict[str, Any]


class DatadogMetricWindowClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, site: Optional[str] = None):
        self.api_key = api_key or os.getenv("DATADOG_API_KEY")
        self.app_key = app_key or os.getenv("DATADOG_APP_KEY")
        self.site = site or os.getenv("DATADOG_SITE", "datadoghq.com")
        if not self.api_key or not self.app_key:
            raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    def query_metric_window(self, metric_name: str, start_time: datetime, end_time: datetime, interval: int = 60) -> List[MetricDatapoint]:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        url = f"https://api.{self.site}/api/v1/query"
        params = {
            "from": int(start_time.timestamp()),
            "to": int(end_time.timestamp()),
            "query": f"avg:{metric_name}{{*}}.rollup(avg,{interval})",
        }
        headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        return self._normalize_datadog_series(payload)

    def _normalize_datadog_series(self, payload: Dict[str, Any]) -> List[MetricDatapoint]:
        series = payload.get("series", [])
        datapoints: List[MetricDatapoint] = []
        for item in series:
            scope = item.get("scope", "")
            dimensions = {"scope": scope} if scope else {}
            for ts, value in item.get("pointlist", []):
                if value is None:
                    continue
                timestamp = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc).isoformat()
                datapoints.append(MetricDatapoint(timestamp=timestamp, value=float(value), dimensions=dimensions))
        return datapoints


def query_metric_window(metric_name: str, hours: int = 1, interval: int = 60) -> List[MetricDatapoint]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    client = DatadogMetricWindowClient()
    return client.query_metric_window(metric_name, start_time, end_time, interval)
