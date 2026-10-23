"""
Summarize recent metric trends or anomalies.

Uses the Anthropic Messages API (api.anthropic.com) with the
claude-3-sonnet-20240229 model to generate natural-language summaries
of metric trends, anomalies, and operational insights.
"""

import os
import json
from typing import List, Optional, Dict, Any

from observability_models import (
    MetricAggregationStats,
    MetricComparisonResult,
    MetricSeries,
    MetricQueryResponse,
)


def _build_metric_context(
    metric_name: str,
    stats: Optional[List[MetricAggregationStats]] = None,
    comparison: Optional[MetricComparisonResult] = None,
    query_response: Optional[MetricQueryResponse] = None,
) -> str:
    """Build a text context block summarizing metric data for the LLM."""
    parts: List[str] = []
    parts.append(f"Metric: {metric_name}")

    if stats:
        for i, s in enumerate(stats):
            parts.append(
                f"\nSeries {i + 1}:"
                f"  min={s.min:.4f}, max={s.max:.4f}, avg={s.avg:.4f},"
                f" sum={s.sum:.4f}, count={s.count},"
                f" p50={s.percentile_50:.4f}, p95={s.percentile_95:.4f}, p99={s.percentile_99:.4f}"
                f"  tags={json.dumps(s.tags)}"
            )

    if comparison:
        parts.append(
            f"\nComparison:"
            f"  mean_diff={comparison.mean_diff:.4f},"
            f" max_diff={comparison.max_diff:.4f},"
            f" min_diff={comparison.min_diff:.4f},"
            f" correlation={comparison.correlation:.4f}"
        )

    if query_response:
        parts.append(
            f"\nQuery returned {query_response.total_datapoints} datapoints"
            f" across {len(query_response.series)} series"
        )
        for s in query_response.series:
            parts.append(f"  - {s.display_name}: {len(s.datapoints)} points")

    return "\n".join(parts)


def summarize_metric_trends(
    metric_name: str,
    stats: Optional[List[MetricAggregationStats]] = None,
    comparison: Optional[MetricComparisonResult] = None,
    query_response: Optional[MetricQueryResponse] = None,
    custom_context: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = "claude-3-sonnet-20240229",
    max_tokens: int = 1024,
) -> str:
    """Summarize recent metric trends or anomalies using Anthropic Claude.

    Sends metric statistics and/or comparison results to the Anthropic
    Messages API (api.anthropic.com) using the claude-3-sonnet-20240229
    model to produce a natural-language operational summary.

    Args:
        metric_name: Name of the metric being analyzed.
        stats: Optional list of MetricAggregationStats.
        comparison: Optional MetricComparisonResult for cross-resource analysis.
        query_response: Optional raw query response for additional context.
        custom_context: Additional free-text context to include.
        api_key: Anthropic ANTHROPIC_API_KEY (defaults to env).
        model: Anthropic model identifier (default: claude-3-sonnet-20240229).
        max_tokens: Maximum tokens in the response.

    Returns:
        Natural-language summary text from the Anthropic model.

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set.
    """
    anthropic_api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required "
            "for Anthropic Messages API access."
        )

    context = _build_metric_context(metric_name, stats, comparison, query_response)
    if custom_context:
        context += f"\n\nAdditional context:\n{custom_context}"

    system_prompt = (
        "You are a senior site reliability engineer analyzing infrastructure metrics. "
        "Provide a concise, actionable summary of the metric trends below. "
        "Highlight any anomalies, concerning patterns, or notable changes. "
        "If correlation between series is low (<0.3), mention the divergence. "
        "Keep the summary professional and focused on operational impact."
    )

    user_message = (
        f"Please analyze the following metric data and provide a summary of trends and anomalies:\n\n{context}"
    )

    # Build the Anthropic Messages API request
    import requests

    headers = {
        "x-api-key": anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_message},
        ],
    }

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()

    data = resp.json()
    # Extract the assistant's text response
    for block in data.get("content", []):
        if block.get("type") == "text":
            return block["text"]

    raise ValueError("No text content returned from Anthropic Messages API")


def summarize_metric_anomaly(
    metric_name: str,
    current_stats: MetricAggregationStats,
    baseline_stats: MetricAggregationStats,
    api_key: Optional[str] = None,
    model: str = "claude-3-sonnet-20240229",
) -> str:
    """Summarize an anomaly by comparing current vs baseline statistics.

    Args:
        metric_name: The metric being analyzed.
        current_stats: Current window aggregated stats.
        baseline_stats: Baseline/historical aggregated stats.
        api_key: Anthropic API key.
        model: Anthropic model identifier.

    Returns:
        Anomaly summary text.
    """
    anomaly_context = (
        f"Metric: {metric_name}\n\n"
        f"Current window stats:\n"
        f"  avg={current_stats.avg:.4f}, p95={current_stats.percentile_95:.4f}, "
        f"p99={current_stats.percentile_99:.4f}, max={current_stats.max:.4f}\n\n"
        f"Baseline stats:\n"
        f"  avg={baseline_stats.avg:.4f}, p95={baseline_stats.percentile_95:.4f}, "
        f"p99={baseline_stats.percentile_99:.4f}, max={baseline_stats.max:.4f}\n\n"
        f"Deviation from baseline avg: {(current_stats.avg - baseline_stats.avg) / max(baseline_stats.avg, 1e-9) * 100:.1f}%"
    )

    return summarize_metric_trends(
        metric_name=metric_name,
        custom_context=anomaly_context,
        api_key=api_key,
        model=model,
        max_tokens=512,
    )
