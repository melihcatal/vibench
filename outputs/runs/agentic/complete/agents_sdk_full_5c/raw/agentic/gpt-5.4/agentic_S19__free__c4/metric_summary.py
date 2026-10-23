from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from aggregate_metric_stats import aggregate_metric_stats
from query_metric_window import query_metric_window
from observability_models import MetricWindowRequest


OPENAI_MODEL = "gpt-4o-mini"


def metric_summary(request: MetricWindowRequest) -> Dict[str, Any]:
    series = query_metric_window(request)
    stats = aggregate_metric_stats(request, statistic="mean")
    values = [point.value for point in series.points]
    trend = "flat"
    if len(values) >= 2:
        if values[-1] > values[0]:
            trend = "upward"
        elif values[-1] < values[0]:
            trend = "downward"

    anomaly_hint = "no obvious anomaly"
    if values:
        peak = max(values)
        if stats.value and peak > stats.value * 1.5:
            anomaly_hint = "spike detected"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize cloud monitoring metric behavior for operators.",
            },
            {
                "role": "user",
                "content": (
                    f"Metric: {request.metric_type}\n"
                    f"Series count: {series.series_count}\n"
                    f"Point count: {len(series.points)}\n"
                    f"Average: {stats.value}\n"
                    f"Trend: {trend}\n"
                    f"Anomaly hint: {anomaly_hint}\n"
                    f"Recent values: {values[-10:]}\n"
                    "Provide a concise operational summary."
                ),
            },
        ],
    )
    return {
        "metric_type": request.metric_type,
        "trend": trend,
        "anomaly_hint": anomaly_hint,
        "summary": response.output_text,
    }
