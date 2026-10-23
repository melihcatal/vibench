from __future__ import annotations

from typing import Any, Dict

from model_client import bedrock_runtime_client, load_config
from model_models import PlatformRequest, normalize_text_response, serialize_prompt



def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    config = load_config()
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=config.bedrock_model_id,
        body=serialize_prompt(request.prompt, request.max_tokens, request.temperature),
        contentType="application/json",
        accept="application/json",
    )
    payload = __import__("json").loads(response["body"].read())
    normalized = normalize_text_response(payload)
    return {
        "text": normalized.text,
        "model_id": normalized.model_id,
        "usage": normalized.usage,
        "resource_id": config.bedrock_model_id,
        "provider_metadata": payload,
        "provider": "Amazon Bedrock",
    }
