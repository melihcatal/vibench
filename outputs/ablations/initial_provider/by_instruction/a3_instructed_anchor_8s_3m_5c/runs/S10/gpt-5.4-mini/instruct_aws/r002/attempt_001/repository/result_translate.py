import json
import os

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import normalize_text


def result_translate(text: str, target_language: str) -> str:
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("translate"),
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": int(os.getenv("TRANSLATE_MAX_TOKENS", "256")),
            "temperature": 0.2,
            "system": f"Translate the user's text into {target_language}.",
            "messages": [{"role": "user", "content": text}],
        }).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return normalize_text(raw.get("content", raw))
