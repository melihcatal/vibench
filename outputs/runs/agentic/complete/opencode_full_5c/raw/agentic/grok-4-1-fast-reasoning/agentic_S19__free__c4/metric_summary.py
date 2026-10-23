import os
import json
from typing import List, Dict, Any
from openai import OpenAI


def generate_metric_summary(
    metric_data: List[Dict[str, Any]], focus: str = "trends and anomalies"
) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    data_str = json.dumps(metric_data)[:8000]
    messages = [
        {
            "role": "system",
            "content": "You are a metrics observability expert. Analyze time series data for trends, anomalies, and insights.",
        },
        {
            "role": "user",
            "content": f"Summarize the following metric data focusing on {focus}:\n{data_str}",
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, max_tokens=500, temperature=0.3
    )
    return response.choices[0].message.content
