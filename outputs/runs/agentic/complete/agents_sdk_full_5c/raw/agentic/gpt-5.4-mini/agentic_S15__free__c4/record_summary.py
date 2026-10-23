from __future__ import annotations

from typing import Any, Dict, Mapping

import boto3

from database_models import extract_field_text


def record_summary(record: Mapping[str, Any]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    text = extract_field_text(record, ["title", "summary", "body", "content"])
    prompt = f"Summarize this document record in one short paragraph:\n{text}"
    response = client.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 120, "temperature": 0.2},
    )
    output = response["output"]["message"]["content"][0]["text"]
    return {"summary": output}
