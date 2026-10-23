from typing import Any, Optional

from model_client import get_bedrock_runtime_client, resolve_model_resource
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    build_bedrock_converse_payload,
)


BEDROCK_DEFAULT_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"


def collect_platform_metadata(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[list[str]] = None,
    inference_profile_arn: Optional[str] = None,
    region: Optional[str] = None,
) -> dict[str, Any]:
    resource = resolve_model_resource(model_id or BEDROCK_DEFAULT_MODEL)
    target_model_id = resource.model_id
    if inference_profile_arn:
        target_model_id = inference_profile_arn

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
    )

    payload = build_bedrock_converse_payload(request)

    response = client.converse(**payload)

    output = response.get("output", {})
    message = output.get("message", {})
    content_blocks = message.get("content", [])
    text_parts = []
    for block in content_blocks:
        if block.get("type") == "text":
            text_parts.append(block.get("text", ""))
    generated_text = "".join(text_parts)

    stop_reason = message.get("stopReason", "end_turn")
    usage = response.get("usage", {})
    input_tokens = usage.get("inputTokens", 0)
    output_tokens = usage.get("outputTokens", 0)
    total_tokens = usage.get("totalTokens", input_tokens + output_tokens)

    request_id = response.get("ResponseMetadata", {}).get("RequestId")

    metrics = response.get("metrics", {})
    latency_ms = metrics.get("latencyMs")

    return {
        "text": generated_text,
        "model_id": resource.model_id,
        "model_arn": resource.model_arn,
        "model_family": resource.model_family,
        "provider": resource.provider,
        "stop_reason": stop_reason,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "request_id": request_id,
        "latency_ms": latency_ms,
        "inference_profile_arn": inference_profile_arn,
        "platform": "aws-bedrock",
        "endpoint": f"bedrock-runtime.{region or 'us-east-1'}.amazonaws.com",
        "raw_response": response,
    }
