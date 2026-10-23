import openai
import os
import json
from typing import Dict, Any
from observability_models import MetricDatapoints


def metric_summary(datapoints: MetricDatapoints) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    serial_datapoints = json.dumps(
        [
            {"timestamp": dp["Timestamp"].isoformat(), "value": dp.get("Average", 0)}
            for dp in datapoints
        ],
        indent=2,
    )
    prompt = f"""Summarize recent metric trends or anomalies from these datapoints:
{serial_datapoints}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content
