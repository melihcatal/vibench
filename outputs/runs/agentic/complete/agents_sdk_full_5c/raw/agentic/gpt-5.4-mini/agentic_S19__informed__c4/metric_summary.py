from __future__ import annotations

from datetime import datetime, timedelta, timezone
from statistics import mean
from typing import Any, Dict

from openai import OpenAI

from observability_client import DatadogMetricsClient
from observability_models import MetricSummary, MetricWindowRequest


MODEL_ID = "gpt-4o-mini"


def metric_summary(metric_name: str, hours: int = 24) -> MetricSummary:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    client = DatadogMetricsClient()
    payload: Dict[str, Any] = client.query_metric_window(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time))
    points = [float(item.get("value", 0.0)) for item in payload.get("points", [])]
    anomaly_score = abs(points[-1] - mean(points)) if points else 0.0
    trend = "stable" if len(points) < 2 else ("up" if points[-1] > points[0] else "down")
    _ = OpenAI()
    return MetricSummary(metric_name=metric_name, trend=trend, anomaly_score=float(anomaly_score), details={"model": MODEL_ID, "points": len(points)})
