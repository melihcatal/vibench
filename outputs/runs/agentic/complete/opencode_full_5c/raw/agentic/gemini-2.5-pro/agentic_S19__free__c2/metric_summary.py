import os
import openai
from typing import List
from observability_models import MetricSeries


def summarize_metric_data(series_list: List[MetricSeries]) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_content = (
        "Summarize the following metric data trends and note any anomalies:\n\n"
    )
    for series in series_list:
        prompt_content += f"Metric: {series.metric_name}\n"
        if series.tags:
            prompt_content += f"Tags: {series.tags}\n"

        values = [p.value for p in series.points]
        avg_val = sum(values) / len(values) if values else 0
        max_val = max(values) if values else 0
        min_val = min(values) if values else 0

        prompt_content += f"  - Average: {avg_val:.2f}\n"
        prompt_content += f"  - Max: {max_val:.2f}\n"
        prompt_content += f"  - Min: {min_val:.2f}\n\n"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful monitoring and observability assistant.",
            },
            {
                "role": "user",
                "content": prompt_content,
            },
        ],
        model="gpt-4-turbo",
    )
    return chat_completion.choices[0].message.content
