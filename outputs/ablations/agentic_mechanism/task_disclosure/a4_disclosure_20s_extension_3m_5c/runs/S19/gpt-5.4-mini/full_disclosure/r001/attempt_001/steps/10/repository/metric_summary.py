import json
import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Sequence

import requests


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


@dataclass
class MetricSummary:
    metric: str
    window_start: datetime
    window_end: datetime
    points: List[MetricPoint]
    min_value: Optional[float]
    max_value: Optional[float]
    average_value: Optional[float]
    delta: Optional[float]
    percent_change: Optional[float]
    trend: str
    anomalies: List[Dict[str, Any]]


class DatadogMetricSummaryClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None, site: Optional[str] = None):
        self.api_key = api_key or os.getenv("DATADOG_API_KEY")
        self.app_key = app_key or os.getenv("DATADOG_APP_KEY")
        self.site = site or os.getenv("DATADOG_SITE", "datadoghq.com")
        if not self.api_key or not self.app_key:
            raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY are required")
        self.base_url = f"https://api.{self.site}"

    def _headers(self) -> Dict[str, str]:
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Accept": "application/json",
        }

    def query_points(self, metric: str, start: datetime, end: datetime, query: Optional[str] = None) -> List[MetricPoint]:
        qs = query or metric
        params = {
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
            "query": qs,
        }
        resp = requests.get(f"{self.base_url}/api/v1/query", headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        series = payload.get("series", [])
        points: List[MetricPoint] = []
        for s in series:
            for ts, value in s.get("pointlist", []):
                if value is None:
                    continue
                points.append(MetricPoint(timestamp=datetime.fromtimestamp(ts, tz=timezone.utc), value=float(value)))
        points.sort(key=lambda p: p.timestamp)
        return points


def _trend(points: Sequence[MetricPoint]) -> str:
    if len(points) < 2:
        return "insufficient-data"
    first = points[0].value
    last = points[-1].value
    if math.isclose(first, last, rel_tol=0.01, abs_tol=0.01):
        return "stable"
    return "increasing" if last > first else "decreasing"


def _anomalies(points: Sequence[MetricPoint]) -> List[Dict[str, Any]]:
    if len(points) < 4:
        return []
    values = [p.value for p in points]
    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    stddev = math.sqrt(variance)
    threshold = 2 * stddev
    anomalies: List[Dict[str, Any]] = []
    for point in points:
        if stddev > 0 and abs(point.value - avg) > threshold:
            anomalies.append(
                {
                    "timestamp": point.timestamp.isoformat(),
                    "value": point.value,
                    "z_score": (point.value - avg) / stddev,
                }
            )
    return anomalies


def summarize_metric(metric: str, hours: int = 24, query: Optional[str] = None, client: Optional[DatadogMetricSummaryClient] = None) -> MetricSummary:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    client = client or DatadogMetricSummaryClient()
    points = client.query_points(metric=metric, start=start, end=end, query=query)
    values = [p.value for p in points]
    min_value = min(values) if values else None
    max_value = max(values) if values else None
    average_value = (sum(values) / len(values)) if values else None
    delta = (values[-1] - values[0]) if len(values) >= 2 else None
    percent_change = ((delta / values[0]) * 100.0) if delta is not None and values[0] != 0 else None
    return MetricSummary(
        metric=metric,
        window_start=start,
        window_end=end,
        points=points,
        min_value=min_value,
        max_value=max_value,
        average_value=average_value,
        delta=delta,
        percent_change=percent_change,
        trend=_trend(points),
        anomalies=_anomalies(points),
    )


def summarize_metric_as_dict(metric: str, hours: int = 24, query: Optional[str] = None, client: Optional[DatadogMetricSummaryClient] = None) -> Dict[str, Any]:
    summary = summarize_metric(metric=metric, hours=hours, query=query, client=client)
    return {
        "metric": summary.metric,
        "window_start": summary.window_start.isoformat(),
        "window_end": summary.window_end.isoformat(),
        "point_count": len(summary.points),
        "min": summary.min_value,
        "max": summary.max_value,
        "average": summary.average_value,
        "delta": summary.delta,
        "percent_change": summary.percent_change,
        "trend": summary.trend,
        "anomalies": summary.anomalies,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize recent Datadog metric trends or anomalies")
    parser.add_argument("metric")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--query", default=None)
    args = parser.parse_args()
    result = summarize_metric_as_dict(metric=args.metric, hours=args.hours, query=args.query)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
