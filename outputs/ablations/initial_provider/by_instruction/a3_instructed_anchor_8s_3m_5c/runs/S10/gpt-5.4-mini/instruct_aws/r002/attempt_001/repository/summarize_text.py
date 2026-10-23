import json
import os
from typing import Any, Dict

from model_client import bedrock_runtime_client, model_id_for_task
from model_models import ChatRequest, ChatResponse, normalize_text


def _payload(request: ChatRequest) -> Dict[str, Any]:
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "system": request.system,
        "messages": [{"role": "user", "content": request.user}],
    }


def summarize_text(text: str) -> ChatResponse:
    request = ChatRequest(
        system="Summarize the provided text clearly and concisely.",
        user=text,
        max_tokens=int(os.getenv("SUMMARY_MAX_TOKENS", "256")),
        temperature=float(os.getenv("SUMMARY_TEMPERATURE", "0.2")),
    )
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("summarize"),
        body=json.dumps(_payload(request)).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return ChatResponse(text=normalize_text(raw.get("content", raw)), raw=raw)
