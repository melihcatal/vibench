from datetime import datetime

from openai import OpenAI


def metric_summary(metric_name: str, values: list[float], timestamp: datetime):
    client = OpenAI()
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize recent metric trends and anomalies."},
            {"role": "user", "content": f"Metric {metric_name} at {timestamp.isoformat()}: {values}"},
        ],
    )
