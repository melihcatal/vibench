from __future__ import annotations

import json
from typing import Any, Dict, List

from openai import OpenAI

from observability_models import SummaryResult


OPENAI_MODEL = "gpt-4o-mini"


def metric_summary(metric_payload: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    series = metric_payload.get("series") or []
    compact_points: List[Dict[str, Any]] = []
    for item in series[:3]:
        for point in (item.get("points") or [])[:10]:
            compact_points.append({"interval_end": point.get("interval_end"), "value": point.get("value"), "labels": point.get("labels")})
    prompt = "Summarize recent metric trends, mention anomalies, and return JSON with keys summary_text, detected_trend, anomaly_flag, supporting_points. Data: " + json.dumps(compact_points)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an SRE analyst for observability metrics."},
            {"role": "user", "content": prompt},
        ],
    )
    parsed = json.loads(response.choices[0].message.content)
    result = SummaryResult(**parsed)
    return result.__dict__
