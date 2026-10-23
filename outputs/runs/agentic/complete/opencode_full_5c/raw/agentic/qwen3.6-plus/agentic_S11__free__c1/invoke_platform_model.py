import time
from typing import Optional

from model_client import get_bedrock_runtime_client, resolve_model_resource
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    normalize_bedrock_response,
    build_bedrock_converse_payload,
)


BEDROCK_DEFAULT_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"


def invoke_platform_model(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[list[str]] = None,
    inference_profile_arn: Optional[str] = None,
    deployment_id: Optional[str] = None,
    region: Optional[str] = None,
) -> PlatformModelResponse:
    resource = resolve_model_resource(model_id or BEDROCK_DEFAULT_MODEL)
    target_model_id = resource.model_id
    if inference_profile_arn:
        target_model_id = inference_profile_arn
    elif deployment_id:
        target_model_id = (
            f"arn:aws:bedrock:{region or 'us-east-1'}::deployment/{deployment_id}"
        )

    client = get_bedrock_runtime_client(region=region)

    request = PlatformModelRequest(
        model_id=target_model_id,
        prompt=prompt,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stop_sequences=stop_sequences,
        inference_profile_arn=inference_profile_arn,
        deployment_id=deployment_id,
    )

    payload = build_bedrock_converse_payload(request)

    start_time = time.time()
    response = client.converse(**payload)
    elapsed_ms = (time.time() - start_time) * 1000

    result = normalize_bedrock_response(response, resource.model_id)
    result.latency_ms = elapsed_ms
    result.resource_arn = resource.model_arn
    return result
