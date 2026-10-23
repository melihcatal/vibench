from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from observability_models import AggregationStats, MetricSeries, format_metric_timeline


OPENAI_MODEL = "gpt-4o"


def summarize_metric_trends(
    series: MetricSeries | None = None,
    stats: AggregationStats | None = None,
    timeline_text: str | None = None,
    anomaly_flags: list[str] | None = None,
    client: OpenAI | None = None,
) -> str:
    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        client = OpenAI(api_key=api_key)

    context_parts = []

    if series:
        context_parts.append(format_metric_timeline(series))

    if stats:
        stat_lines = [
            f"Aggregation for {stats.metric}:",
            f"  avg={stats.avg}, min={stats.min_}, max={stats.max_}, count={stats.count}",
            f"  p50={stats.p50}, p95={stats.p95}, p99={stats.p99}",
        ]
        context_parts.append("\n".join(stat_lines))

    if timeline_text:
        context_parts.append(f"Timeline data:\n{timeline_text}")

    if anomaly_flags:
        context_parts.append(f"Detected anomalies: {', '.join(anomaly_flags)}")

    context = (
        "\n\n".join(context_parts) if context_parts else "No metric data provided."
    )

    system_prompt = (
        "You are an observability analyst. Summarize recent metric trends, "
        "highlight anomalies, and provide actionable insights. Be concise."
    )

    user_prompt = (
        f"Analyze the following metric data and provide a summary:\n\n{context}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    from observability_models import DataPoint
    import time

    now = int(time.time())
    pts = [
        DataPoint(timestamp=now - 300 + i * 60, value=50.0 + i * 2.5) for i in range(10)
    ]
    sample_series = MetricSeries(
        metric="system.cpu.user",
        display_name="CPU User %",
        expression="avg:system.cpu.user",
        unit="percent",
        scope="env:production,host:web-01",
        start_ts=now - 3600,
        end_ts=now,
        interval=60,
        points=pts,
    )
    summary = summarize_metric_trends(series=sample_series)
    print(summary)
