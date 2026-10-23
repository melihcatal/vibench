"""
metric_summary.py - Summarize recent metric trends or anomalies.
Uses Google Gemini API (generativelanguage.googleapis.com) for LLM inference.
Provider: Google Gemini API
SDK: google-generativeai
Auth: GOOGLE_API_KEY
Model: gemini-1.5-flash
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from observability_client import (
    DatadogConfig,
    DatadogMetricsClient,
    build_windowed_request,
)
from observability_models import MetricQueryResponse, compute_series_stats


GEMINI_MODEL = "gemini-1.5-flash"

SYSTEM_PROMPT = """You are a metrics analyst assistant. Given metric data from an
observability platform, summarize recent trends, identify anomalies, and provide
actionable insights. Focus on:
1. Overall trend direction (increasing, decreasing, stable)
2. Notable spikes or dips
3. Pattern observations (periodic, random, correlated)
4. Recommendations for investigation or action
Be concise and specific. Use the actual metric values in your analysis."""


def get_metric_data(
    metric_name: str,
    window_minutes: int = 60,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Fetch metric data from Datadog and return a structured summary."""
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_windowed_request(
        metric_name=metric_name,
        window_minutes=window_minutes,
        aggregation="avg",
        rollup=60,
        tags=tags,
    )

    response = client.query(request)

    summary: Dict[str, Any] = {
        "metric": metric_name,
        "window_minutes": window_minutes,
        "series": [],
    }

    for series in response.series:
        stats = compute_series_stats(series)
        summary["series"].append({
            "scope": series.scope,
            "display_name": series.display_name,
            "unit": series.unit,
            "point_count": stats.count,
            "avg": round(stats.avg, 4),
            "min": round(stats.min, 4),
            "max": round(stats.max, 4),
            "stddev": round(stats.stddev, 4) if stats.stddev else None,
            "recent_values": [round(p.value, 4) for p in series.points[-10:]],
        })

    return summary


def summarize_metrics(
    metric_name: str,
    window_minutes: int = 60,
    tags: Optional[List[str]] = None,
    google_api_key: Optional[str] = None,
) -> str:
    """
    Summarize recent metric trends using Google Gemini API.

    Args:
        metric_name: The Datadog metric identifier.
        window_minutes: Time window in minutes.
        tags: Optional tag filters.
        google_api_key: Optional API key override (falls back to GOOGLE_API_KEY env).

    Returns:
        Generated summary text from Gemini.
    """
    api_key = google_api_key or os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    metric_data = get_metric_data(metric_name, window_minutes, tags)

    user_prompt = (
        f"Analyze the following metric data from Datadog (monitoring service) "
        f"and provide a trend summary:\n\n"
        f"Metric: {metric_name}\n"
        f"Window: Last {window_minutes} minutes\n\n"
        f"Data:\n{json.dumps(metric_data, indent=2)}"
    )

    response = model.generate_content(
        [SYSTEM_PROMPT, user_prompt],
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 1024,
        },
    )

    return response.text


def main():
    if len(sys.argv) < 2:
        print("Usage: metric_summary.py <metric_name> [--window MINUTES] [--tags TAG1 TAG2]")
        sys.exit(1)

    metric_name = sys.argv[1]
    window = 60
    tags = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--window" and i + 1 < len(sys.argv):
            window = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
            tags = sys.argv[i + 1].split(",")
            i += 2
        else:
            i += 1

    summary = summarize_metrics(metric_name, window, tags)
    print(summary)


if __name__ == "__main__":
    main()
