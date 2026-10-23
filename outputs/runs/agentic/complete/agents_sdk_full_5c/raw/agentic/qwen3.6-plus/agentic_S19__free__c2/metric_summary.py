"""
Summarize recent metric trends or anomalies.

Provider: Datadog (datadog-api-client) with OpenAI API for summarization.
Uses datadog_api_client.v1.api.metrics_api.MetricsApi for metric data
and openai OpenAI client for trend anomaly summarization via api.openai.com.
"""

from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import openai

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi

from observability_client import ObservabilityClient
from observability_models import (
    MetricDataPoint,
    MetricSeries,
    MetricTimeWindow,
    normalize_datadog_response,
)


def _detect_anomalies(
    data_points: List[MetricDataPoint],
    z_threshold: float = 2.0,
    min_points: int = 10,
) -> List[Dict[str, Any]]:
    """Detect anomalies using z-score method."""
    if len(data_points) < min_points:
        return []

    values = [dp.value for dp in data_points]
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = variance ** 0.5

    if std == 0:
        return []

    anomalies = []
    for dp in data_points:
        z_score = (dp.value - mean) / std
        if abs(z_score) > z_threshold:
            anomalies.append({
                "timestamp": dp.timestamp.isoformat(),
                "value": dp.value,
                "z_score": round(z_score, 3),
                "direction": "above" if z_score > 0 else "below",
            })
    return anomalies


def _compute_trend(data_points: List[MetricDataPoint]) -> Dict[str, Any]:
    """Compute simple linear regression trend."""
    if len(data_points) < 2:
        return {"direction": "flat", "slope": 0.0, "r_squared": 0.0}

    n = len(data_points)
    timestamps = [dp.timestamp.timestamp() for dp in data_points]
    values = [dp.value for dp in data_points]

    # Normalize timestamps to reduce numerical issues
    t0 = timestamps[0]
    x = [t - t0 for t in timestamps]

    x_mean = sum(x) / n
    y_mean = sum(values) / n

    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, values))
    denominator = sum((xi - x_mean) ** 2 for xi in x)

    if denominator == 0:
        return {"direction": "flat", "slope": 0.0, "r_squared": 0.0}

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, values))
    ss_tot = sum((yi - y_mean) ** 2 for yi in values)

    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    direction = "increasing" if slope > 0.001 else ("decreasing" if slope < -0.001 else "flat")

    return {
        "direction": direction,
        "slope": round(slope * 3600, 6),  # slope per hour
        "r_squared": round(r_squared, 4),
    }


def metric_summary(
    metric_name: str,
    window: Optional[MetricTimeWindow] = None,
    tags: Optional[Dict[str, str]] = None,
    openai_model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize recent metric trends and anomalies using Datadog data and OpenAI.

    1. Queries metric data from Datadog via datadog_api_client SDK (api.datadoghq.com).
    2. Computes statistical trends and detects anomalies.
    3. Uses OpenAI (api.openai.com) with gpt-4o-mini to generate a natural-language summary.

    Args:
        metric_name: Datadog metric name.
        window: Time window; defaults to last 60 minutes.
        tags: Optional tag filters.
        openai_model: OpenAI model to use, default gpt-4o-mini.
        api_key: Datadog API key.
        app_key: Datadog App key.
        openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var).

    Returns:
        Dict with trend, anomalies, stats_summary, and ai_summary.
    """
    if window is None:
        window = MetricTimeWindow.from_now(minutes_ago=60)

    oa_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")

    # Query Datadog for metric data
    client = ObservabilityClient(api_key=api_key, app_key=app_key)
    try:
        metrics_api: MetricsApi = client.get_v1_api()

        query = f"avg:{metric_name}"
        if tags:
            tag_parts = [f"{k}:{v}" for k, v in tags.items()]
            query += "{" + ",".join(tag_parts) + "}"

        start_ts = int(window.start.timestamp())
        end_ts = int(window.end.timestamp())

        raw_response = metrics_api.query_metrics(_from=start_ts, to=end_ts, query=query)
        data_points = normalize_datadog_response(raw_response)
    finally:
        client.close()

    if not data_points:
        return {
            "metric_name": metric_name,
            "window": {"start": window.start.isoformat(), "end": window.end.isoformat()},
            "trend": {"direction": "unknown", "slope": 0.0, "r_squared": 0.0},
            "anomalies": [],
            "stats_summary": {"count": 0, "message": "No data points found."},
            "ai_summary": "No metric data available for the specified time window.",
        }

    # Compute trend and anomalies
    trend = _compute_trend(data_points)
    anomalies = _detect_anomalies(data_points)

    values = [dp.value for dp in data_points]
    stats = {
        "count": len(data_points),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "avg": round(sum(values) / len(values), 4),
        "std": round((sum((v - sum(values) / len(values)) ** 2 for v in values) / len(values)) ** 0.5, 4),
    }

    # Build prompt for OpenAI gpt-4o-mini
    stats_text = (
        f"Metric: {metric_name}\n"
        f"Time Window: {window.start.isoformat()} to {window.end.isoformat()}\n"
        f"Data Points: {stats['count']}\n"
        f"Min: {stats['min']}, Max: {stats['max']}, Avg: {stats['avg']}, Std Dev: {stats['std']}\n"
        f"Trend: {trend['direction']} (slope: {trend['slope']} per hour, R²: {trend['r_squared']})\n"
    )
    if anomalies:
        stats_text += f"Anomalies Detected: {len(anomalies)}\n"
        for anom in anomalies[:5]:
            stats_text += f"  - {anom['timestamp']}: value={anom['value']}, z={anom['z_score']}, {anom['direction']} mean\n"
    else:
        stats_text += "No anomalies detected.\n"

    prompt = (
        f"You are a DevOps monitoring assistant. Analyze the following metric data and "
        f"provide a concise summary of the recent behavior, including trend, anomalies, "
        f"and any actionable insights:\n\n{stats_text}\n\n"
        f"Provide a 2-3 sentence summary suitable for a dashboard alert or status page."
    )

    ai_summary = ""
    if oa_key:
        try:
            openai_client = openai.OpenAI(api_key=oa_key)
            response = openai_client.chat.completions.create(
                model=openai_model,
                messages=[
                    {"role": "system", "content": "You are a DevOps monitoring expert analyzing Datadog metrics."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.3,
            )
            ai_summary = response.choices[0].message.content.strip() if response.choices else ""
        except Exception:
            ai_summary = f"Automated summary unavailable. {trend['direction'].capitalize()} trend detected " \
                        f"with {len(anomalies)} anomalies over {stats['count']} data points."

    return {
        "metric_name": metric_name,
        "window": {"start": window.start.isoformat(), "end": window.end.isoformat()},
        "trend": trend,
        "anomalies": anomalies,
        "stats_summary": stats,
        "ai_summary": ai_summary,
    }
