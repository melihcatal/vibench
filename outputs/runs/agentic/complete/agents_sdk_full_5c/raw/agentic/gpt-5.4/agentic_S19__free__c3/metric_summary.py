from __future__ import annotations

from typing import Optional

from openai import OpenAI

from query_metric_window import query_metric_window


OPENAI_MODEL = "gpt-4o-mini"


def metric_summary(
    metric_type: str,
    minutes: int = 60,
    project_id: Optional[str] = None,
) -> str:
    window = query_metric_window(metric_type=metric_type, minutes=minutes, project_id=project_id)
    values = window.values()
    latest_values = values[-12:]
    prompt = {
        "metric_type": metric_type,
        "sample_count": len(values),
        "recent_values": latest_values,
        "average": window.avg(),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize infrastructure metrics and mention trend direction and possible anomalies in one concise paragraph.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return response.output_text
