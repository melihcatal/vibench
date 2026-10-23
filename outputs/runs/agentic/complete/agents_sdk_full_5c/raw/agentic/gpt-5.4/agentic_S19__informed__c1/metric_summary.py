from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

from observability_models import points_to_serializable
from query_metric_window import query_metric_window


OPENAI_MODEL = os.getenv("OPENAI_METRIC_SUMMARY_MODEL", "gpt-4o-mini")



def metric_summary(request) -> Dict[str, Any]:
    series = query_metric_window(request)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "metric_name": series.metric_name,
        "namespace": series.namespace,
        "dimensions": series.dimensions,
        "source": "Amazon CloudWatch",
        "datapoints": points_to_serializable(series.datapoints),
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize recent metric behavior, trend direction, volatility, and notable anomalies in concise operational language.",
            },
            {
                "role": "user",
                "content": str(prompt),
            },
        ],
    )
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODEL,
        "summary": response.output_text,
        "series_points": len(series.datapoints),
    }
