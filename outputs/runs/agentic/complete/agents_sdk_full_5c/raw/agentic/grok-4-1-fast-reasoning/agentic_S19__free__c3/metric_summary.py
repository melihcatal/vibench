import openai
import os
import json
from typing import List
from dataclasses import asdict
from observability_models import MetricDatapoint

def metric_summary(
    datapoints: List[MetricDatapoint],
    prompt_suffix: str = ""
) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    data_json = json.dumps([asdict(dp) for dp in datapoints], default=str)
    prompt = f"""Summarize recent metric trends or anomalies from these datapoints:

{data_json}

Provide a concise summary of trends, changes, or potential anomalies.{prompt_suffix}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content