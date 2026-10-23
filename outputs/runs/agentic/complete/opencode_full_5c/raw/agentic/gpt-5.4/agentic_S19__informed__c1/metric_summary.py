from __future__ import annotations

import json
from typing import Any, Dict, List

from openai import OpenAI


def metric_summary(
    metric_name: str,
    series: List[Dict[str, Any]],
    anomaly_hints: List[str] | None = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    prompt = {
        "metric_name": metric_name,
        "series": series,
        "anomaly_hints": anomaly_hints or [],
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You summarize infrastructure metrics and call out notable trend shifts and anomalies in concise JSON.",
            },
            {"role": "user", "content": json.dumps(prompt)},
        ],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    parsed = json.loads(content)
    return {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "summary": parsed,
    }
