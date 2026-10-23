import os
import json
from typing import Optional

import anthropic

from observability_models import MetricQueryResponse, MetricSeries


ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def _build_metric_context(response: MetricQueryResponse) -> str:
    lines = []
    lines.append(
        f"Metric query results for time window {response.from_ts} to {response.to_ts}:"
    )
    for series in response.series:
        lines.append(
            f"\nSeries: {series.metric_name} (scope: {series.scope}, aggregation: {series.aggregation})"
        )
        point_count = len(series.points)
        lines.append(f"  Total datapoints: {point_count}")
        if series.points:
            values = [p.value for p in series.points]
            lines.append(
                f"  First value: {values[0]} at {series.points[0].timestamp.isoformat()}"
            )
            lines.append(
                f"  Last value: {values[-1]} at {series.points[-1].timestamp.isoformat()}"
            )
            lines.append(
                f"  Min: {min(values)}, Max: {max(values)}, Avg: {sum(values) / len(values):.4f}"
            )
            if len(values) >= 2:
                trend = (
                    "increasing"
                    if values[-1] > values[0]
                    else "decreasing"
                    if values[-1] < values[0]
                    else "stable"
                )
                lines.append(f"  Overall trend: {trend}")
    return "\n".join(lines)


def summarize_metric_trends(
    metric_response: MetricQueryResponse,
    prompt: Optional[str] = None,
) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic Claude API"
        )

    context = _build_metric_context(metric_response)
    default_prompt = (
        "You are a metrics monitoring analyst. Analyze the following metric data and provide "
        "a concise summary of recent trends, anomalies, and notable patterns. "
        "Highlight any significant spikes, drops, or sustained deviations. "
        "Keep the summary under 200 words and use bullet points for key findings."
    )
    system_prompt = prompt or default_prompt

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": context}],
    )
    return message.content[0].text


def summarize_metric_anomalies(
    metric_response: MetricQueryResponse,
    threshold_sigma: float = 2.0,
) -> str:
    anomaly_context_lines = []
    for series in metric_response.series:
        values = [p.value for p in series.points]
        if len(values) < 3:
            continue
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance**0.5
        if std == 0:
            continue
        anomalies = []
        for p in series.points:
            z_score = abs(p.value - mean) / std
            if z_score > threshold_sigma:
                anomalies.append(
                    f"    - At {p.timestamp.isoformat()}: value={p.value:.4f}, z-score={z_score:.2f}"
                )
        if anomalies:
            anomaly_context_lines.append(
                f"\nAnomalies in {series.metric_name} ({series.scope}):"
            )
            anomaly_context_lines.extend(anomalies)

    if not anomaly_context_lines:
        return "No anomalies detected above the configured threshold."

    anomaly_text = "\n".join(anomaly_context_lines)
    return summarize_metric_trends(
        metric_response=metric_response,
        prompt=(
            f"You are a metrics anomaly detection analyst. The following anomalies were detected "
            f"using a {threshold_sigma}-sigma threshold:\n\n{anomaly_text}\n\n"
            "Provide a brief assessment of these anomalies and their potential operational impact."
        ),
    )
