from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from openai import OpenAI


def metric_summary(
    metric_name: str, recent_values: list[float], notes: str = ""
) -> Dict[str, Any]:
    client = OpenAI()
    prompt = f"Summarize trends and anomalies for metric {metric_name}. Values: {recent_values}. Notes: {notes}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return {"metric": metric_name, "summary": response.choices[0].message.content}
