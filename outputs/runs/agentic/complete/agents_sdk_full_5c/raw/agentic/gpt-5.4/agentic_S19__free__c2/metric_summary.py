from __future__ import annotations

import json
from typing import List

from observability_client import bedrock_runtime_client, load_config
from observability_models import TrendSummary


BEDROCK_SERVICE = "bedrock-runtime.amazonaws.com"


def metric_summary(metric_name: str, window_start, window_end, datapoints: List[dict]) -> TrendSummary:
    cfg = load_config()
    client = bedrock_runtime_client()
    prompt = {
        "metric_name": metric_name,
        "window_start": str(window_start),
        "window_end": str(window_end),
        "datapoints": datapoints,
        "task": "Return compact JSON with keys direction, anomaly_detected, latest_value, average_value.",
    }
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": json.dumps(prompt)}],
            }
        ],
    }
    response = client.invoke_model(modelId=cfg.bedrock_model_id, body=json.dumps(body))
    payload = json.loads(response["body"].read())
    text = "".join(block.get("text", "") for block in payload.get("content", []))
    parsed = json.loads(text)
    return TrendSummary(
        metric_name=metric_name,
        window_start=window_start,
        window_end=window_end,
        point_count=len(datapoints),
        latest_value=parsed.get("latest_value"),
        average_value=parsed.get("average_value"),
        direction=parsed.get("direction", "flat"),
        anomaly_detected=bool(parsed.get("anomaly_detected", False)),
        provider=BEDROCK_SERVICE,
    )
