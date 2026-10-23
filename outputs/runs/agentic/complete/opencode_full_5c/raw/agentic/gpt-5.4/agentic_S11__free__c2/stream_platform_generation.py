from __future__ import annotations

from typing import Dict, Iterator

from model_client import get_bedrock_client
from model_models import GenerationRequest, build_messages, build_system_prompts
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: GenerationRequest) -> Iterator[Dict]:
    resource = select_platform_resource()
    client = get_bedrock_client(resource.region_name)
    response = client.converse_stream(
        modelId=resource.inference_profile_arn,
        system=build_system_prompts(request),
        messages=build_messages(request),
        inferenceConfig={
            "temperature": request.temperature,
            "maxTokens": request.max_tokens,
        },
    )
    for event in response["stream"]:
        yield event
