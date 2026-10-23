import json
import os
from typing import Any, Dict

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import ChatRequest, extract_json_like, normalize_text


def extract_json(text: str) -> Dict[str, Any]:
    request = ChatRequest(
        system="Extract structured JSON matching the user's content. Return only JSON.",
        user=text,
        max_tokens=int(os.getenv("JSON_MAX_TOKENS", "256")),
        temperature=0.0,
    )
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("extract_json"),
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system": request.system,
            "messages": [{"role": "user", "content": request.user}],
        }).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return extract_json_like(normalize_text(raw.get("content", raw)))
