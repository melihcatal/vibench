from __future__ import annotations

from openai import OpenAI

from aggregate_metric_stats import aggregate_metric_stats
from observability_models import MetricWindowRequest


def metric_summary(request: MetricWindowRequest) -> str:
    stats = aggregate_metric_stats(request)
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You summarize production monitoring metrics and flag brief anomaly hints.",
            },
            {
                "role": "user",
                "content": (
                    f"Metric: {stats.metric_type}\n"
                    f"Window: {stats.start_time} to {stats.end_time}\n"
                    f"Samples: {stats.sample_count}\n"
                    f"Min: {stats.minimum}\n"
                    f"Max: {stats.maximum}\n"
                    f"Average: {stats.average}\n"
                    f"Total: {stats.total}\n"
                    "Summarize recent trend and note if the numbers suggest a spike, drop, or stable behavior."
                ),
            },
        ],
    )
    return response.output_text
