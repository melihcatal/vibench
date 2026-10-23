import json
import os

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import normalize_text


def spoken_brief(text: str) -> str:
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("spoken"),
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": int(os.getenv("SPOKEN_MAX_TOKENS", "128")),
            "temperature": 0.2,
            "system": "Rewrite the text as a short spoken brief suitable for audio narration.",
            "messages": [{"role": "user", "content": text}],
        }).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return normalize_text(raw.get("content", raw))
