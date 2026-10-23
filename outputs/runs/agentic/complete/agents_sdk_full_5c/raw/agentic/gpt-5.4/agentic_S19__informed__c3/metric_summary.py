from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from observability_models import MetricSummaryResult


def metric_summary(metric_payload: Dict[str, Any]) -> MetricSummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    datapoints: List[Dict[str, Any]] = metric_payload.get("datapoints", [])
    prompt = {
        "task": "Summarize recent metric trends and flag anomalies.",
        "metric": metric_payload,
        "instructions": "Return JSON with keys summary_text, trend, anomaly_flag.",
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You analyze observability metrics for production systems."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
    )
    content = response.choices[0].message.content
    parsed = json.loads(content)
    return MetricSummaryResult(
        summary_text=parsed["summary_text"],
        trend=parsed["trend"],
        anomaly_flag=bool(parsed["anomaly_flag"]),
        datapoint_count=len(datapoints),
    )
