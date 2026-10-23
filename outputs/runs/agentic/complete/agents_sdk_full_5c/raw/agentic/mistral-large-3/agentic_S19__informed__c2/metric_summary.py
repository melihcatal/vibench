from openai import OpenAI
from observability_models import MetricStats, MetricDataPoint
from typing import List
import os


def metric_summary(metric_name: str, datapoints: List[MetricDataPoint], stats: MetricStats) -> str:
    """Summarize recent metric trends or anomalies using OpenAI GPT-3.5-turbo."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Summarize the following metric data for {metric_name}:

Recent datapoints (timestamp: value):
{', '.join([f'{dp.timestamp}: {dp.value}' for dp in datapoints[-10:]])}

Statistics:
- Count: {stats.count}
- Average: {stats.avg:.2f}
- Min: {stats.min:.2f}
- Max: {stats.max:.2f}

Provide a concise summary of trends, anomalies, or notable observations.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()