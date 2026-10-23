from __future__ import annotations

from model_client import get_bedrock_client
from model_models import (
    GenerationRequest,
    normalize_bedrock_converse_response,
    build_messages,
    build_system_prompts,
)
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: GenerationRequest):
    resource = select_platform_resource()
    client = get_bedrock_client(resource.region_name)
    response = client.converse(
        modelId=resource.inference_profile_arn,
        system=build_system_prompts(request),
        messages=build_messages(request),
        inferenceConfig={
            "temperature": request.temperature,
            "maxTokens": request.max_tokens,
        },
    )
    return normalize_bedrock_converse_response(
        response, resource.model_id, resource.inference_profile_arn
    )
