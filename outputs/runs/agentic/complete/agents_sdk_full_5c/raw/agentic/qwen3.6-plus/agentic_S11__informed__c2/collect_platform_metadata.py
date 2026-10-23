"""
[SAME-SCENARIO] Returns model output together with Amazon Bedrock provider
platform metadata such as usage, resource IDs, or model handles.

Provider: Amazon Bedrock
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
import time
from typing import Optional

from model_client import get_bedrock_runtime_client, resolve_model_id
from model_models import (
    PlatformRequest,
    PlatformResponse,
    PlatformMetadata,
    build_user_message,
)


def invoke_with_metadata(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> dict:
    """Invoke an Amazon Bedrock model and return output with full metadata.

    Provider signals: boto3 bedrock-runtime converse API, Bedrock usage block
    (inputTokens, outputTokens, totalTokens), ResponseMetadata RequestId,
    Bedrock model identifiers.

    Returns:
        {
            "output_text": str,
            "metadata": PlatformMetadata,
            "model_id": str,
            "provider": "amazon-bedrock",
        }
    """
    client = get_bedrock_runtime_client(region_name=region)
    resolved_model = resolve_model_id(model_id) if model_id else "anthropic.claude-3-5-sonnet-20241022-v2:0"

    request = PlatformRequest(
        model_id=resolved_model,
        messages=[build_user_message(prompt)],
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    payload = request.to_bedrock_payload()

    start_time = time.time()
    response = client.converse(**payload)
    elapsed_ms = (time.time() - start_time) * 1000

    platform_response = PlatformResponse.from_bedrock_response(response)
    metadata = PlatformMetadata.from_bedrock_response(response)
    metadata.latency_ms = elapsed_ms

    # Also capture the request ID from Bedrock's response metadata
    response_metadata = response.get("ResponseMetadata", {})
    metadata.request_id = response_metadata.get("RequestId", "")

    return {
        "output_text": platform_response.output_text,
        "metadata": metadata,
        "model_id": resolved_model,
        "provider": "amazon-bedrock",
        "stop_reason": platform_response.stop_reason,
        "latency_ms": metadata.latency_ms,
    }


def invoke_with_detailed_metadata(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> dict:
    """Invoke a Bedrock model with enriched metadata including raw provider response.

    Provider signals: Amazon Bedrock Converse API, modelId, usage metrics,
    HTTP status code, retry count, and Bedrock-specific response structure.

    Returns dict with:
    - output_text: generated text
    - input_tokens, output_tokens, total_tokens: usage counts
    - model_id: resolved Bedrock model identifier
    - request_id: AWS request ID
    - http_status_code: response HTTP status
    - stop_reason: Bedrock stop reason
    - provider_response: full raw Bedrock response dict
    """
    client = get_bedrock_runtime_client(region_name=region)
    resolved_model = resolve_model_id(model_id) if model_id else "anthropic.claude-3-5-sonnet-20241022-v2:0"

    request = PlatformRequest(
        model_id=resolved_model,
        messages=[build_user_message(prompt)],
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    payload = request.to_bedrock_payload()

    start_time = time.time()
    response = client.converse(**payload)
    elapsed_ms = (time.time() - start_time) * 1000

    usage = response.get("usage", {})
    response_metadata = response.get("ResponseMetadata", {})
    platform_response = PlatformResponse.from_bedrock_response(response)

    return {
        "output_text": platform_response.output_text,
        "input_tokens": usage.get("inputTokens", 0),
        "output_tokens": usage.get("outputTokens", 0),
        "total_tokens": usage.get("totalTokens", 0),
        "model_id": resolved_model,
        "provider": "amazon-bedrock",
        "request_id": response_metadata.get("RequestId", ""),
        "http_status_code": response_metadata.get("HTTPStatusCode"),
        "stop_reason": response.get("stopReason"),
        "latency_ms": elapsed_ms,
        "provider_response": response,
    }


def batch_invoke_with_metadata(
    prompts: list[str],
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> list[dict]:
    """Batch invoke Amazon Bedrock and collect metadata for each call.

    Provider signals: boto3 bedrock-runtime converse, Bedrock model identifiers,
    per-request usage tracking.
    """
    results = []
    for prompt in prompts:
        result = invoke_with_metadata(
            prompt=prompt,
            model_id=model_id,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            region=region,
        )
        results.append(result)
    return results
