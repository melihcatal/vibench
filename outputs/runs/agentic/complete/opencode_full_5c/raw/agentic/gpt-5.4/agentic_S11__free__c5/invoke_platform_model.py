from __future__ import annotations

from model_client import get_bedrock_runtime_client, resolve_runtime_model_identifier
from model_models import (
    ModelRequest,
    ModelResponse,
    extract_usage,
    normalize_converse_output,
)
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    resource = select_platform_resource()
    runtime_client = get_bedrock_runtime_client(resource.region_name)
    response = runtime_client.converse(
        modelId=resolve_runtime_model_identifier(resource),
        messages=[{"role": "user", "content": [{"text": request.prompt}]}],
        inferenceConfig={
            "maxTokens": request.max_tokens,
            "temperature": request.temperature,
        },
    )
    return ModelResponse(
        text=normalize_converse_output(response),
        model_id=resource.model_id,
        resource_id=resource.inference_profile_arn or resource.model_id,
        usage=extract_usage(response),
        raw_response=response,
    )
