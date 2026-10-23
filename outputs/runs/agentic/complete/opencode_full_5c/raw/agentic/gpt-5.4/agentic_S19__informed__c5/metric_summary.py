from __future__ import annotations

from openai.types.chat import ChatCompletion

from observability_client import openai_client
from observability_models import MetricPoint, MetricSummaryResponse


def metric_summary(
    metric_name: str, points: list[MetricPoint]
) -> MetricSummaryResponse:
    client = openai_client()
    serialized_points = [
        {"timestamp": point.timestamp, "value": point.value, "unit": point.unit}
        for point in points
    ]
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You summarize CloudWatch metric trends and flag anomalies. Return JSON with summary, detected_anomaly, rationale.",
            },
            {
                "role": "user",
                "content": f"Metric: {metric_name}\nPoints: {serialized_points}",
            },
        ],
    )
    content = (
        completion.choices[0].message.content
        or '{"summary":"","detected_anomaly":false,"rationale":""}'
    )
    import json

    payload = json.loads(content)
    return MetricSummaryResponse(
        summary=str(payload.get("summary", "")),
        detected_anomaly=bool(payload.get("detected_anomaly", False)),
        rationale=str(payload.get("rationale", "")),
    )
