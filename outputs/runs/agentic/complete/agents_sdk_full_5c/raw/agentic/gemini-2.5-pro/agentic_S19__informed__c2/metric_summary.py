import os
from openai import OpenAI
from typing import List
from observability_models import TimeSeries

def summarize_metric_data(time_series_data: List[TimeSeries]) -> str:
    """
    Uses an LLM to generate a human-readable summary of metric trends or anomalies.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set.")

    client = OpenAI(api_key=api_key)

    prompt_content = "Summarize the following metric data, highlighting any potential anomalies or significant trends:\n\n"
    for series in time_series_data:
        prompt_content += f"Metric: {series.metric_name}\n"
        prompt_content += f"Resource: {series.resource_labels}\n"
        points_str = ", ".join([f"({p.timestamp.isoformat()}, {p.value:.2f})" for p in series.points])
        prompt_content += f"Data points: {points_str}\n\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes monitoring data."},
            {"role": "user", "content": prompt_content},
        ],
    )

    return response.choices[0].message.content
