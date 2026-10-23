from __future__ import annotations

import json
import os
from statistics import mean
from typing import List

from openai import OpenAI

from observability_models import MetricPoint, MetricSummary, point_to_dict


MODEL = "gpt-4.1-mini"


def _detect_anomalies(points: List[MetricPoint]) -> List[str]:
    values = [point.value for point in points]
    if len(values) < 3:
        return []
    baseline = mean(values[:-1]) if len(values) > 1 else values[-1]
    latest = values[-1]
    anomalies = []
    if baseline and abs(latest - baseline) / abs(baseline) >= 0.5:
        anomalies.append(
            f"Latest value {latest:.3f} deviates materially from baseline {baseline:.3f}"
        )
    if latest == max(values):
        anomalies.append("Latest value is the peak for the selected window")
    if latest == min(values):
        anomalies.append("Latest value is the trough for the selected window")
    return anomalies


def metric_summary(points: List[MetricPoint]) -> MetricSummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    anomalies = _detect_anomalies(points)
    payload = json.dumps([point_to_dict(point) for point in points[-20:]])
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize recent monitoring metric trends in 2 sentences and mention notable anomalies if present.",
            },
            {
                "role": "user",
                "content": f"Metric points: {payload}\nDetected anomalies: {json.dumps(anomalies)}",
            },
        ],
    )
    return MetricSummary(
        summary_text=response.output_text,
        detected_anomalies=anomalies,
        provider_model=MODEL,
    )
