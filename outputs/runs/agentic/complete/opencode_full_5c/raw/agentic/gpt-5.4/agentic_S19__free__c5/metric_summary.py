from __future__ import annotations

import json

from observability_client import extract_gemini_text, gemini_generate
from observability_models import MetricSummary, MetricWindowRequest
from query_metric_window import query_metric_window


def metric_summary(request: MetricWindowRequest) -> MetricSummary:
    series = query_metric_window(request)
    values = [point.value for entry in series for point in entry.points]
    latest_value = values[-1] if values else None
    baseline_average = (
        (sum(values[:-1]) / len(values[:-1])) if len(values) > 1 else latest_value
    )
    prompt = json.dumps(
        {
            "task": "Summarize metric trend and anomaly state",
            "metric_type": request.metric_type,
            "values": values[-20:],
            "instructions": "Return compact JSON with keys trend, anomaly_detected, message.",
        }
    )
    response = gemini_generate("gemini-1.5-pro", prompt)
    text = extract_gemini_text(response)
    parsed = json.loads(text) if text else {}
    return MetricSummary(
        metric_type=request.metric_type,
        trend=parsed.get("trend", "stable"),
        anomaly_detected=bool(parsed.get("anomaly_detected", False)),
        latest_value=latest_value,
        baseline_average=baseline_average,
        message=parsed.get("message", ""),
    )
