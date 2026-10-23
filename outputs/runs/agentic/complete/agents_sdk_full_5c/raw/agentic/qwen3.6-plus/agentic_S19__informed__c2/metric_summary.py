"""
Summarize recent metric trends or anomalies using Anthropic Claude API.

Analyzes metric series data and generates natural language summaries
of trends, patterns, and potential anomalies.
Provider: Anthropic (ANTHROPIC_API_KEY, claude-3-sonnet-20240229).
"""

import json
import os
from typing import Optional

from anthropic import Anthropic

from observability_models import MetricSeries, MetricAggregation

ANTHROPIC_MODEL = "claude-3-sonnet-20240229"


def _get_anthropic_client() -> Anthropic:
    """Create an authenticated Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is required")
    return Anthropic(api_key=api_key)


def summarize_metric_trend(
    series: MetricSeries,
    max_tokens: int = 512,
) -> str:
    """
    Generate a natural language summary of metric trends using Anthropic Claude.

    Args:
        series: MetricSeries with datapoints to analyze.
        max_tokens: Maximum tokens for the response.

    Returns:
        Human-readable trend summary.
    """
    client = _get_anthropic_client()

    values = series.values
    timestamps = [t.isoformat() for t in series.timestamps]
    data_summary = {
        "metric": series.metric,
        "point_count": len(values),
        "values": values[-50:] if len(values) > 50 else values,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "tags": series.tag_set,
    }

    prompt = (
        f"Analyze the following metric data from Datadog and provide a concise summary "
        f"of trends, patterns, and any anomalies detected.\n\n"
        f"Metric: {series.metric}\n"
        f"Tags: {series.tag_set}\n"
        f"Data points: {len(values)}\n"
        f"Recent values (last 50): {json.dumps(values[-50:])}\n\n"
        f"Please provide:\n"
        f"1. Overall trend direction (increasing, decreasing, stable)\n"
        f"2. Notable patterns or cycles\n"
        f"3. Any anomalies or outliers detected\n"
        f"4. Brief recommendation if concerning behavior is detected"
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        temperature=0.3,
        system="You are an expert SRE analyst. Summarize metric data concisely.",
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def summarize_multiple_metrics(
    aggregations: list[MetricAggregation],
    max_tokens: int = 1024,
) -> str:
    """
    Generate a comparative summary of multiple metric aggregations using Anthropic Claude.

    Args:
        aggregations: List of MetricAggregation objects to summarize.
        max_tokens: Maximum tokens for the response.

    Returns:
        Comparative analysis summary.
    """
    client = _get_anthropic_client()

    agg_data = []
    for agg in aggregations:
        agg_data.append({
            "metric": agg.metric,
            "avg": agg.avg,
            "min": agg.min_val,
            "max": agg.max_val,
            "count": agg.count,
            "tags": agg.tag_set,
            "percentiles": agg.percentiles,
        })

    prompt = (
        f"Analyze the following Datadog metric aggregations and provide a comparative summary.\n\n"
        f"Metrics:\n{json.dumps(agg_data, indent=2)}\n\n"
        f"Provide:\n"
        f"1. Comparison of metric behaviors\n"
        f"2. Identify metrics with concerning patterns\n"
        f"3. Suggested areas for investigation"
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        temperature=0.3,
        system="You are an expert SRE analyst providing comparative metric analysis.",
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def detect_anomalies_in_series(
    series: MetricSeries,
    sensitivity: str = "medium",
    max_tokens: int = 512,
) -> str:
    """
    Use Anthropic Claude to detect and describe anomalies in metric series data.

    Args:
        series: MetricSeries to analyze for anomalies.
        sensitivity: Detection sensitivity (low, medium, high).
        max_tokens: Maximum response tokens.

    Returns:
        Anomaly detection summary.
    """
    client = _get_anthropic_client()

    values = series.values
    if len(values) < 3:
        return "Insufficient data points for anomaly detection."

    prompt = (
        f"Perform anomaly detection on the following Datadog metric series "
        f"with {sensitivity} sensitivity.\n\n"
        f"Metric: {series.metric}\n"
        f"Values: {json.dumps(values)}\n\n"
        f"Identify any anomalous data points, describe their characteristics, "
        f"and estimate the severity of each anomaly found."
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        temperature=0.2,
        system="You are a metrics anomaly detection expert. Be precise and factual.",
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
