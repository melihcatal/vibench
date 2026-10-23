from __future__ import annotations

import json
from typing import Any, Dict

from openai import OpenAI

from aggregate_metric_stats import aggregate_metric_stats
from query_metric_window import query_metric_window



def metric_summary(metric_type: str, minutes: int = 60, project_id: str | None = None) -> Dict[str, Any]:
    window = query_metric_window(metric_type=metric_type, minutes=minutes, project_id=project_id)
    stats = aggregate_metric_stats(metric_type=metric_type, minutes=minutes, project_id=project_id)
    client = OpenAI()
    prompt = {
        "metric_type": metric_type,
        "window": window,
        "statistics": stats,
        "task": "Summarize trend, volatility, and any anomalies in 4 concise bullets.",
    }
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "You are an SRE assistant that summarizes cloud monitoring signals."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4o-mini",
        "summary": response.output_text,
        "metric_type": metric_type,
    }
