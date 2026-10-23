from __future__ import annotations

from openai import OpenAI

from observability_client import ObservabilityConfig
from observability_models import MetricSummary, MetricWindowRequest


def metric_summary(request: MetricWindowRequest) -> MetricSummary:
    cfg = ObservabilityConfig()
    client = OpenAI()
    prompt = f"Summarize the recent trend for metric {request.metric_name} in namespace {cfg.namespace}."
    response = client.chat.completions.create(
        model=cfg.llm_model_id,
        messages=[{"role": "system", "content": "You summarize cloud metrics."}, {"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content or "steady"
    trend = "rising" if "up" in text.lower() else "steady"
    return MetricSummary(metric_name=request.metric_name, trend=trend, anomaly_score=0.0, latest_value=None, window_start=request.start_time, window_end=request.end_time)
