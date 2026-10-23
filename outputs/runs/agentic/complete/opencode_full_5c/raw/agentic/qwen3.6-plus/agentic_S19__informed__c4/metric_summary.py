import os
import json
from typing import Optional

import anthropic

from observability_models import (
    MetricSummaryRequest,
    MetricSummaryResponse,
    Datapoint,
)

ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def get_anthropic_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic Messages API"
        )
    return anthropic.Anthropic(api_key=api_key)


def summarize_metric_trends(request: MetricSummaryRequest) -> MetricSummaryResponse:
    client = get_anthropic_client()
    trend_points = [
        {"timestamp": dp.timestamp, "value": dp.value}
        for dp in request.trend_data[-100:]
    ]
    anomaly_context = (
        json.dumps(request.anomalies, indent=2)
        if request.anomalies
        else "No anomalies detected."
    )
    values_summary = []
    if trend_points:
        vals = [p["value"] for p in trend_points]
        values_summary = [
            f"Total points: {len(vals)}",
            f"Min: {min(vals):.4f}",
            f"Max: {max(vals):.4f}",
            f"Avg: {sum(vals) / len(vals):.4f}",
        ]
    prompt = (
        f"Analyze the following metric data for '{request.metric_name}' over the last {request.time_window_hours} hours.\n\n"
        f"Metric statistics:\n" + "\n".join(values_summary) + "\n\n"
        f"Recent datapoints (last {len(trend_points)}):\n"
        f"{json.dumps(trend_points[:20], indent=2)}\n\n"
        f"Detected anomalies:\n{anomaly_context}\n\n"
        f"Provide a concise summary of:\n"
        f"1. Overall trend direction (increasing, decreasing, stable, volatile)\n"
        f"2. Key observations about the metric behavior\n"
        f"3. Any notable anomalies or patterns\n"
        f"4. Potential operational implications\n\n"
        f"Respond in a structured format with clear sections."
    )
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        temperature=0.3,
        system="You are a metrics analysis assistant. Provide concise, data-driven summaries of infrastructure metrics.",
        messages=[{"role": "user", "content": prompt}],
    )
    summary_text = message.content[0].text
    trend_direction = "stable"
    for line in summary_text.lower().split("\n"):
        if "increasing" in line or "upward" in line or "rising" in line:
            trend_direction = "increasing"
            break
        elif "decreasing" in line or "downward" in line or "declining" in line:
            trend_direction = "decreasing"
            break
        elif "volatile" in line or "fluctuating" in line:
            trend_direction = "volatile"
            break
    anomaly_descriptions = []
    for anomaly in request.anomalies:
        desc = f"Anomaly at timestamp {anomaly.get('timestamp', 'unknown')}: {anomaly.get('description', anomaly.get('type', 'unknown'))}"
        anomaly_descriptions.append(desc)
    if not anomaly_descriptions and "no anomalies" not in summary_text.lower():
        anomaly_descriptions = [summary_text.split("\n\n")[-1]] if summary_text else []
    return MetricSummaryResponse(
        summary_text=summary_text,
        anomaly_descriptions=anomaly_descriptions,
        trend_direction=trend_direction,
        status="ok",
    )


if __name__ == "__main__":
    sample_data = [
        Datapoint(timestamp=int(time.time()) - i * 300, value=50.0 + (i % 10) * 2.5)
        for i in range(20)
    ]
    req = MetricSummaryRequest(
        metric_name="system.cpu.user",
        trend_data=sample_data,
        anomalies=[
            {
                "timestamp": sample_data[5].timestamp,
                "type": "spike",
                "description": "CPU spike detected",
            }
        ],
        time_window_hours=1,
    )
    result = summarize_metric_trends(req)
    print(f"Trend: {result.trend_direction}")
    print(f"Summary:\n{result.summary_text}")
