from __future__ import annotations

from typing import Any, Dict

from model_client import bedrock_runtime_client, load_config
from model_models import PlatformRequest, normalize_text_response, serialize_prompt



def invoke_platform_model(request: PlatformRequest) -> Dict[str, Any]:
    config = load_config()
    client = bedrock_runtime_client()
    body = serialize_prompt(request.prompt, request.max_tokens, request.temperature)
    kwargs: Dict[str, Any] = {
        "modelId": config.bedrock_model_id,
        "body": body,
        "contentType": "application/json",
        "accept": "application/json",
    }
    if config.guardrail_identifier and config.guardrail_version:
        kwargs["guardrailIdentifier"] = config.guardrail_identifier
        kwargs["guardrailVersion"] = config.guardrail_version
    response = client.invoke_model(**kwargs)
    payload = response["body"].read()
    normalized = normalize_text_response(__import__("json").loads(payload))
    return {
        "text": normalized.text,
        "model_id": normalized.model_id,
        "usage": normalized.usage,
        "raw_metadata": normalized.metadata,
        "provider": "Amazon Bedrock",
    }
