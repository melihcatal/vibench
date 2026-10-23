import os
import openai
import json
from typing import List, Dict, Any


def metric_summary(datapoints: List[Dict[str, Any]], metric_name: str) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Summarize recent trends, anomalies, or key insights from the following {metric_name} metric datapoints:

{json.dumps(datapoints, default=str, indent=2)}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in observability and metrics analysis. Provide a concise summary of trends, changes, and potential anomalies.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
