import json
import os

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import normalize_text


def prompt_safety(text: str) -> bool:
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("safety"),
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": int(os.getenv("SAFETY_MAX_TOKENS", "64")),
            "temperature": 0.0,
            "system": "Classify whether the text is unsafe. Reply with SAFE or UNSAFE.",
            "messages": [{"role": "user", "content": text}],
        }).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    verdict = normalize_text(raw.get("content", raw)).upper()
    return "SAFE" in verdict and "UNSAFE" not in verdict
