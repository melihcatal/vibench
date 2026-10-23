import os
from datetime import datetime
from typing import List
import google.generativeai as genai

from observability_models import MetricSeries, MetricAggregationResult


def summarize_metric_trends(
    metric_data: List[MetricSeries],
    aggregation_data: List[MetricAggregationResult],
    additional_context: str = "",
) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    prompt_parts = [
        "Given the following metric data and aggregated statistics, summarize recent trends or anomalies. "
        "Focus on identifying significant changes, patterns, or deviations from expected behavior. "
        "Also, consider the provided additional context if available."
    ]

    prompt_parts.append("\n--- Metric Series Data ---")
    for series in metric_data:
        prompt_parts.append(f"Labels: {series.labels}")
        for point in series.points[-5:]:  # Limit to last 5 points for brevity
            prompt_parts.append(f"  Time: {point.time}, Value: {point.value}")

    prompt_parts.append("\n--- Aggregated Statistics ---")
    for agg in aggregation_data:
        prompt_parts.append(
            f"Metric Type: {agg.metric_type}, Labels: {agg.labels}, Mean: {agg.mean}, Max: {agg.max}, Min: {agg.min}"
        )

    if additional_context:
        prompt_parts.append(f"\n--- Additional Context ---")
        prompt_parts.append(additional_context)

    response = model.generate_content("\n".join(prompt_parts))
    return response.text
