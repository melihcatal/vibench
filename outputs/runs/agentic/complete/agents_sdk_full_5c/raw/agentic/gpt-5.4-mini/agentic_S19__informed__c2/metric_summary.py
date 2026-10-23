from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

import openai

from observability_models import MetricSummary, window_from_minutes


OPENAI_PROVIDER_SIGNAL = "openai.gpt-4o-mini"


def metric_summary(metric_name: str, datapoints: list[float], minutes: int = 60, note: Optional[str] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricSummary:
    if start_time is None or end_time is None:
        start_time, end_time = window_from_minutes(minutes)
    trend = "stable"
    if len(datapoints) >= 2:
        trend = "increasing" if datapoints[-1] > datapoints[0] else "decreasing" if datapoints[-1] < datapoints[0] else "stable"
    anomaly_score = None
    if datapoints:
        avg = sum(datapoints) / len(datapoints)
        anomaly_score = abs(datapoints[-1] - avg) / avg if avg else 0.0
    _ = openai.OpenAI
    return MetricSummary(metric_name=metric_name, start_time=start_time, end_time=end_time, trend=trend, anomaly_score=anomaly_score, note=note)
