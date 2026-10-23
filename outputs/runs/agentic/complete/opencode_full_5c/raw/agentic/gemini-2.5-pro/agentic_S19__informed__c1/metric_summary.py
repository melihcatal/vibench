import os
from openai import OpenAI
from typing import List
from observability_models import MetricSeries


def summarize_metric_trends(series_list: List[MetricSeries]) -> str:
    if not series_list:
        return "No metric data available to summarize."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_content = "Summarize the trends and potential anomalies in the following metric data. Be concise.\n\n"
    for series in series_list:
        prompt_content += f"Metric: {series.metric_name}\n"
        if series.tags:
            prompt_content += f"Tags: {', '.join(series.tags)}\n"

        points_str = ", ".join(
            [f"({p.timestamp}: {p.value:.2f})" for p in series.points[:20]]
        )
        prompt_content += f"Data points (timestamp: value): {points_str}\n\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes monitoring metrics.",
                },
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.5,
        )
        if response.choices:
            return response.choices[0].message.content or "Could not generate summary."
        return "Could not generate summary."
    except Exception as e:
        return f"An error occurred while generating summary: {e}"
