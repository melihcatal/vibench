import os
from typing import List
from openai import OpenAI
from observability_models import MetricDatapoint


def metric_summary(
    datapoints: List[MetricDatapoint], summary_type: str = "trends and anomalies"
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    data_str = "\n".join(
        [
            f"Time: {p.timestamp.isoformat()}, Average: {p.average}, Min: {p.minimum}, Max: {p.maximum}, Sum: {p.sum_}"
            for p in datapoints
            if p.average is not None
        ]
    )
    messages = [
        {
            "role": "system",
            "content": "You are an observability expert analyzing metric trends and detecting anomalies.",
        },
        {
            "role": "user",
            "content": f"Summarize recent {summary_type} based on this time series data:\n{data_str}",
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0.3, max_tokens=500
    )
    return response.choices[0].message.content
