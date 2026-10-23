from __future__ import annotations

import os
from datetime import datetime

from openai import OpenAI

from aggregate_metric_stats import aggregate_metric_stats
from query_metric_window import query_metric_window


def metric_summary(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    project_id: str | None = None,
    resource_type: str | None = None,
    filter_clauses: list[str] | None = None,
) -> str:
    stats = aggregate_metric_stats(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        project_id=project_id,
        resource_type=resource_type,
        filter_clauses=filter_clauses,
    )
    window = query_metric_window(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        project_id=project_id,
        resource_type=resource_type,
        filter_clauses=filter_clauses,
    )
    condensed = []
    for series in window.series[:5]:
        condensed.append(
            {
                "series_name": series.series_name,
                "resource_labels": series.resource_labels,
                "metric_labels": series.metric_labels,
                "points": [
                    {"t": p.interval_end, "v": p.value} for p in series.points[:20]
                ],
            }
        )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You summarize cloud monitoring metrics and point out trends, spikes, drops, and anomalous behavior in concise operational language.",
            },
            {
                "role": "user",
                "content": f"Metric type: {metric_type}\nStats: {stats}\nSeries: {condensed}",
            },
        ],
    )
    return response.output_text
