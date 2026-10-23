from __future__ import annotations

import json
from typing import Dict

from security_client import get_bedrock_runtime_client
from security_models import PayloadSafetyResult


GUARD_MODEL_ID = "amazon.titan-text-premier-v1:0"


def payload_safety(text: str) -> PayloadSafetyResult:
    bedrock = get_bedrock_runtime_client()
    prompt = (
        "Classify whether the decrypted payload is unsafe. Respond as JSON with keys "
        "safe (boolean), action (string), and categories (object). Text: " + text
    )
    body = {
        "inputText": prompt,
        "textGenerationConfig": {"maxTokenCount": 256, "temperature": 0},
    }
    response = bedrock.invoke_model(
        modelId=GUARD_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )
    raw = json.loads(response["body"].read())
    output_text = raw.get("results", [{}])[0].get("outputText", "{}")
    parsed: Dict[str, object] = json.loads(output_text)
    return PayloadSafetyResult(
        provider="amazon-bedrock",
        safe=bool(parsed.get("safe", False)),
        categories=dict(parsed.get("categories", {})),
        action=str(parsed.get("action", "review")),
    )


def run(text: str) -> dict:
    result = payload_safety(text)
    return result.__dict__
