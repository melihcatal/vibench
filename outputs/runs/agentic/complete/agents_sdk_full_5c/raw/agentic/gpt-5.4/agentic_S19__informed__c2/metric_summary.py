from __future__ import annotations

import os
from typing import List

from anthropic import Anthropic

from query_metric_window import query_metric_window
from observability_models import TrendSummary


MODEL_NAME = "claude-3-5-haiku-20241022"


def metric_summary(project_id: str, metric_type: str, minutes: int = 30) -> TrendSummary:
    metric_window = query_metric_window(project_id=project_id, metric_type=metric_type, minutes=minutes)
    values: List[float] = [point.value for point in metric_window.points]
    if not values:
        return TrendSummary(summary="No recent datapoints available.", anomaly_detected=False, datapoint_count=0)

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = (
        f"Summarize the trend for Google Cloud Monitoring metric {metric_type}. "
        f"Recent datapoints: {values[-50:]}. "
        "Respond in one concise paragraph and end with 'ANOMALY: yes' or 'ANOMALY: no'."
    )
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=180,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(block.text for block in response.content if hasattr(block, "text")).strip()
    anomaly_detected = "ANOMALY: yes" in text.lower() or "anomaly: yes" in text.lower()
    return TrendSummary(summary=text, anomaly_detected=anomaly_detected, datapoint_count=len(values))
