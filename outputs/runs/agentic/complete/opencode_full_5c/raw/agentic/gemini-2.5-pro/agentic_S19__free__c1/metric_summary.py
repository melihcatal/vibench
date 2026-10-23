import os
import cohere
from typing import List
from observability_models import MetricTimeSeries


def summarize_metric_data(time_series_data: List[MetricTimeSeries]) -> str:
    """
    Summarizes metric time series data using the Cohere API.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    prompt_text = (
        "Summarize the following metric data, noting any trends or anomalies:\n\n"
    )
    for series in time_series_data:
        prompt_text += f"Metric: {series.metric_name}\n"
        prompt_text += f"Dimensions: {series.dimensions}\n"
        points_str = ", ".join(
            [f"({p.timestamp}: {p.value:.2f})" for p in series.points]
        )
        prompt_text += f"Data points: {points_str}\n\n"

    response = co.summarize(
        text=prompt_text, model="command", length="medium", extractiveness="low"
    )

    return response.summary
