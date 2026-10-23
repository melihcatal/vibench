from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from aggregate_metric_stats import aggregate_metric_stats
from observability_models import MetricWindowRequest
from query_metric_window import query_metric_window


def metric_summary(request: MetricWindowRequest) -> Dict[str, Any]:
    series = query_metric_window(request)
    stats = aggregate_metric_stats(request)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "metric": request.metric,
        "namespace": request.namespace,
        "stat": request.stat,
        "window": {"start": request.start_iso(), "end": request.end_iso()},
        "points": [
            {"timestamp": p.timestamp, "value": p.value, "unit": p.unit}
            for p in series.points
        ],
        "aggregate": {
            "sample_count": stats.sample_count,
            "minimum": stats.minimum,
            "maximum": stats.maximum,
            "average": stats.average,
            "sum": stats.sum,
            "unit": stats.unit,
        },
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize metric trends and call out anomalies succinctly in JSON.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {"summary": response.output_text, "series": series, "aggregate": stats}
