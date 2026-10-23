"""Summarize recent metric trends or anomalies.

Uses the Anthropic Messages API (anthropic SDK) with the claude-3-sonnet-20240229
model to generate natural-language summaries of metric trends, anomalies, and
observations from a set of time-series data.
Provider signals:
  - anthropic.Anthropic client
  - claude-3-sonnet-20240229 model identifier
  - ANTHROPIC_API_KEY environment variable
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

import anthropic

from observability_models import MetricSeries, compute_series_stats


def summarize_metric_trends(
    series_list: List[MetricSeries],
    metric_name: str,
    window_description: str = "last 60 minutes",
    api_key: Optional[str] = None,
    model: str = "claude-3-sonnet-20240229",
) -> str:
    """Summarize recent metric trends or anomalies using the Anthropic
    Messages API (Claude model).

    Parameters
    ----------
    series_list : list[MetricSeries]
        Normalized metric series to summarize.
    metric_name : str
        Human-readable name of the metric.
    window_description : str
        Description of the time window (e.g. "last 60 minutes").
    api_key : str, optional
        ANTHROPIC_API_KEY; falls back to environment variable.
    model : str
        Anthropic model identifier (default: claude-3-sonnet-20240229).

    Returns
    -------
    str
        Natural-language summary of trends and anomalies.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY is required for Anthropic API access.")

    client = anthropic.Anthropic(api_key=key)

    payload = _build_metric_summary_payload(series_list, metric_name, window_description)

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0.3,
        system=(
            "You are a site reliability engineer summarizing metric data. "
            "Provide concise, actionable observations about trends, spikes, "
            "and potential anomalies. Focus on what changed and what it might mean."
        ),
        messages=[{"role": "user", "content": payload}],
    )

    return message.content[0].text if message.content else "No summary generated."


def _build_metric_summary_payload(
    series_list: List[MetricSeries],
    metric_name: str,
    window_description: str,
) -> str:
    """Build a text payload describing metric series statistics for the LLM."""
    lines = [
        f"Metric: {metric_name}",
        f"Window: {window_description}",
        "",
        "Series data:",
    ]
    for idx, series in enumerate(series_list):
        stats = compute_series_stats(series)
        lines.append(f"  Series {idx + 1}:")
        lines.append(f"    Resource labels: {series.resource_labels}")
        lines.append(f"    Datapoints: {stats['count']}")
        lines.append(f"    Min: {stats['min']:.4f}")
        lines.append(f"    Max: {stats['max']:.4f}")
        lines.append(f"    Mean: {stats['mean']:.4f}")
        lines.append(f"    Sum: {stats['sum']:.4f}")
        if series.points:
            recent = series.points[-5:]
            lines.append(f"    Recent values: {[p.value for p in recent]}")
        lines.append("")

    lines.append(
        "Please summarize the key trends, any anomalies or spikes, and "
        "potential operational implications."
    )
    return "\n".join(lines)


def summarize_anomalies(
    series_list: List[MetricSeries],
    metric_name: str,
    threshold_sigma: float = 2.0,
    api_key: Optional[str] = None,
    model: str = "claude-3-sonnet-20240229",
) -> str:
    """Identify and summarize anomalies in metric series using Anthropic Claude.

    Parameters
    ----------
    series_list : list[MetricSeries]
        Metric series data.
    metric_name : str
        Human-readable metric name.
    threshold_sigma : float
        Standard deviation multiplier for anomaly detection context.
    api_key : str, optional
        ANTHROPIC_API_KEY.
    model : str
        Anthropic model identifier.

    Returns
    -------
    str
        Summary of detected anomalies.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY is required for Anthropic API access.")

    client = anthropic.Anthropic(api_key=key)

    anomaly_data = _extract_anomaly_candidates(series_list, metric_name, threshold_sigma)

    message = client.messages.create(
        model=model,
        max_tokens=768,
        temperature=0.2,
        system=(
            "You are an incident analyst. Review metric data points flagged "
            "as potential anomalies and describe them in a clear, structured format."
        ),
        messages=[{"role": "user", "content": anomaly_data}],
    )

    return message.content[0].text if message.content else "No anomalies detected."


def _extract_anomaly_candidates(
    series_list: List[MetricSeries],
    metric_name: str,
    threshold_sigma: float,
) -> str:
    """Extract points that deviate significantly from the series mean."""
    import math

    lines = [f"Metric: {metric_name}", f"Anomaly threshold: {threshold_sigma} standard deviations", ""]
    for idx, series in enumerate(series_list):
        stats = compute_series_stats(series)
        if stats["count"] < 2:
            continue
        mean = stats["mean"]
        variance = sum((p.value - mean) ** 2 for p in series.points) / stats["count"]
        std = math.sqrt(variance) if variance > 0 else 0.0
        threshold = threshold_sigma * std

        anomalies = [
            p for p in series.points if abs(p.value - mean) > threshold and std > 0
        ]
        lines.append(f"  Series {idx + 1}: {len(anomalies)} potential anomalies out of {stats['count']} points")
        for a in anomalies:
            lines.append(f"    {a.timestamp} value={a.value:.4f} deviation={abs(a.value - mean):.4f}")

    lines.append("\nDescribe each anomaly and its potential impact.")
    return "\n".join(lines)


if __name__ == "__main__":
    sample_series = MetricSeries(
        metric_type="cpu/utilization",
        resource_labels={"instance_id": "vm-001"},
        points=[],
    )
    summary = summarize_metric_trends([sample_series], "CPU Utilization")
    print(summary)
