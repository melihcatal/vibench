from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from observability_models import MetricSeries


OPENAI_MODEL_ID = "gpt-4o"


def summarize_metric_trends(
    series_list: list[MetricSeries],
    metric_name: str,
    prompt_template: str | None = None,
) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)
    data_points_summary = []
    for s in series_list:
        values = [p.value for p in s.points]
        if not values:
            continue
        data_points_summary.append(
            f"Metric: {s.metric}, Scope: {s.scope}, "
            f"Points: {len(values)}, Min: {min(values):.4f}, "
            f"Max: {max(values):.4f}, Avg: {sum(values) / len(values):.4f}"
        )
    data_text = (
        "\n".join(data_points_summary)
        if data_points_summary
        else "No data points available."
    )
    default_prompt = (
        f"Analyze the following metric data for '{metric_name}' and summarize "
        f"recent trends, anomalies, or notable patterns. Keep the summary concise.\n\n"
        f"{data_text}"
    )
    system_prompt = (
        "You are an observability analyst. Summarize metric trends, "
        "identify anomalies, and highlight notable patterns."
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_template or default_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    summary_text = response.choices[0].message.content
    return {
        "metric": metric_name,
        "summary": summary_text,
        "model": OPENAI_MODEL_ID,
        "series_count": len(series_list),
    }
