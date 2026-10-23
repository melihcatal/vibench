from __future__ import annotations

from datetime import timedelta

from openai import OpenAI

from observability_client import DatadogMetricsClient, utc_now
from observability_models import MetricSummary

MODEL_ID = "gpt-4o-mini"


def metric_summary(metric_name: str, minutes: int = 120) -> MetricSummary:
    end_time = utc_now()
    client = DatadogMetricsClient()
    payload = client.query_series(
        __import__("observability_models").observability_models.MetricWindowRequest(
            metric_name=metric_name,
            start_time=end_time - timedelta(minutes=minutes),
            end_time=end_time,
        )
    )
    points = (payload.get("series") or [{}])[0].get("pointlist", [])
    values = [p[1] for p in points if isinstance(p, list) and len(p) > 1]
    trend = "stable"
    if len(values) >= 2 and values[-1] > values[0]:
        trend = "upward"
    elif len(values) >= 2 and values[-1] < values[0]:
        trend = "downward"
    anomaly_score = 0.0
    if values:
        average = sum(values) / len(values)
        anomaly_score = max(abs(v - average) for v in values) / (average or 1.0)
    llm = OpenAI()
    response = llm.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize metric trends and anomalies concisely."},
            {"role": "user", "content": f"Metric: {metric_name}\nTrend: {trend}\nAnomaly score: {anomaly_score:.3f}"},
        ],
    )
    summary = response.choices[0].message.content or ""
    return MetricSummary(metric_name=metric_name, trend=trend, anomaly_score=anomaly_score, summary=summary, raw=payload)
