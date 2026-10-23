import os
import json
from typing import Any

from mistralai import Mistral

from observability_models import (
    MetricTimeSeries,
    MetricDataPoint,
    MetricAggregationResult,
)
from observability_client import load_config

MISTRAL_MODEL = "mistral-large-latest"


def _build_metric_context(
    metric_name: str,
    time_series: MetricTimeSeries,
    aggregation: MetricAggregationResult | None = None,
) -> str:
    lines = []
    lines.append(f"Metric: {metric_name}")
    if time_series.unit:
        lines.append(f"Unit: {time_series.unit}")
    if time_series.points:
        lines.append(f"Data points count: {len(time_series.points)}")
        lines.append(
            f"Time range: {time_series.points[0].timestamp} to {time_series.points[-1].timestamp}"
        )
        values = [p.value for p in time_series.points]
        lines.append(f"Min value: {min(values):.4f}")
        lines.append(f"Max value: {max(values):.4f}")
        lines.append(f"Avg value: {sum(values) / len(values):.4f}")
        if len(values) >= 2:
            deltas = [values[i + 1] - values[i] for i in range(len(values) - 1)]
            max_increase = max(deltas)
            max_decrease = min(deltas)
            lines.append(f"Largest single-step increase: {max_increase:.4f}")
            lines.append(f"Largest single-step decrease: {max_decrease:.4f}")
    if aggregation:
        lines.append(f"\nAggregation ({aggregation.aggregation_type.value}):")
        lines.append(f"  Value: {aggregation.value:.4f}")
        lines.append(f"  Sample count: {aggregation.sample_count}")
        lines.append(f"  Min: {aggregation.min_value:.4f}")
        lines.append(f"  Max: {aggregation.max_value:.4f}")
        lines.append(f"  Avg: {aggregation.avg_value:.4f}")
        lines.append(f"  Sum: {aggregation.sum_value:.4f}")
    return "\n".join(lines)


def _detect_anomalies_simple(time_series: MetricTimeSeries) -> list[dict[str, Any]]:
    anomalies = []
    values = [p.value for p in time_series.points]
    if len(values) < 4:
        return anomalies
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std_dev = variance**0.5
    if std_dev == 0:
        return anomalies
    for i, point in enumerate(time_series.points):
        z_score = abs(point.value - mean) / std_dev
        if z_score > 2.5:
            anomalies.append(
                {
                    "timestamp": point.timestamp,
                    "value": point.value,
                    "z_score": round(z_score, 4),
                    "direction": "above" if point.value > mean else "below",
                }
            )
    return anomalies


def summarize_metric_trends(
    metric_name: str,
    time_series: MetricTimeSeries,
    aggregation: MetricAggregationResult | None = None,
    api_key: str | None = None,
    model: str = MISTRAL_MODEL,
) -> str:
    api_key = api_key or os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        raise ValueError(
            "Mistral API key not configured. Set MISTRAL_API_KEY environment variable."
        )
    context = _build_metric_context(metric_name, time_series, aggregation)
    anomalies = _detect_anomalies_simple(time_series)
    anomaly_text = ""
    if anomalies:
        anomaly_text = "\n\nDetected anomalies:\n"
        for a in anomalies:
            anomaly_text += (
                f"  - At timestamp {a['timestamp']}: value={a['value']:.4f}, "
                f"z-score={a['z_score']}, direction={a['direction']}\n"
            )
    else:
        anomaly_text = (
            "\n\nNo statistical anomalies detected (within 2.5 standard deviations)."
        )
    prompt = (
        f"You are a metrics monitoring analyst. Analyze the following metric data and provide "
        f"a concise summary of recent trends, patterns, and any notable observations.\n\n"
        f"{context}{anomaly_text}\n\n"
        f"Provide your analysis in 3-5 sentences covering:\n"
        f"1. Overall trend direction (increasing, decreasing, stable)\n"
        f"2. Notable patterns or fluctuations\n"
        f"3. Any anomalies or outliers\n"
        f"4. A brief recommendation or observation if applicable"
    )
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful metrics analyst that provides concise, data-driven summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content


def summarize_metric_trends_from_api(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    tags: list[str] | None = None,
    api_key: str | None = None,
    model: str = MISTRAL_MODEL,
) -> str:
    from query_metric_window import query_metric_window
    from aggregate_metric_stats import aggregate_metric_stats

    time_series = query_metric_window(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tags=tags or [],
    )
    aggregation = aggregate_metric_stats(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tags=tags or [],
    )
    return summarize_metric_trends(
        metric_name=metric_name,
        time_series=time_series,
        aggregation=aggregation,
        api_key=api_key,
        model=model,
    )


if __name__ == "__main__":
    metric = os.environ.get("DD_METRIC_NAME", "system.cpu.user")
    summary = summarize_metric_trends_from_api(
        metric,
        start_timestamp=int(__import__("time").time()) - 3600,
        end_timestamp=int(__import__("time").time()),
    )
    print(f"Summary for {metric}:\n{summary}")
