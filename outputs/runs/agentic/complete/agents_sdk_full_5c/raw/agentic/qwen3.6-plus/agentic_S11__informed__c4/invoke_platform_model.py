"""Invoke a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.

Invokes an Amazon Bedrock foundation model using the Bedrock Runtime API with
boto3. Handles request construction, model invocation, and response parsing
for the managed model platform workflow.

Provider: Amazon Bedrock
SDK: boto3 (bedrock-runtime client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
import os
from typing import Optional

from model_client import create_bedrock_runtime_client, resolve_bedrock_credentials
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    parse_bedrock_response,
    normalize_prompt_for_bedrock,
)


def invoke_bedrock_model(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[list] = None,
    region: Optional[str] = None,
) -> PlatformModelResponse:
    """Invoke an Amazon Bedrock foundation model with the given prompt.

    Args:
        prompt: User prompt to send to the model.
        model_id: Bedrock model identifier (defaults to claude-3-sonnet).
        system_prompt: Optional system prompt for the model.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.
        top_p: Top-p sampling parameter.
        stop_sequences: Optional list of stop sequences.
        region: AWS region override.

    Returns:
        PlatformModelResponse with generated text and metadata.

    Raises:
        ValueError: If prompt is empty or invalid.
        Exception: If Bedrock invocation fails.
    """
    if model_id is None:
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    normalized_prompt = normalize_prompt_for_bedrock(prompt)

    request = PlatformModelRequest(
        prompt=normalized_prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stop_sequences=stop_sequences,
    )

    credentials = resolve_bedrock_credentials()
    if region:
        credentials["region_name"] = region

    client = create_bedrock_runtime_client(credentials)

    payload = request.to_bedrock_payload()

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(response["body"].read())

    result = parse_bedrock_response(response_body, model_id)
    result.metadata["request_id"] = response.get("ResponseMetadata", {}).get("RequestId", "")
    result.metadata["invocation_latency"] = response.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("x-amzn-requestid", "")

    return result


def invoke_with_retry(
    prompt: str,
    model_id: Optional[str] = None,
    max_retries: int = 3,
    **kwargs,
) -> PlatformModelResponse:
    """Invoke Bedrock model with automatic retry on transient errors.

    Args:
        prompt: User prompt.
        model_id: Bedrock model identifier.
        max_retries: Maximum retry attempts.
        **kwargs: Additional arguments passed to invoke_bedrock_model.

    Returns:
        PlatformModelResponse on success.

    Raises:
        Exception: If all retries fail.
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            return invoke_bedrock_model(prompt=prompt, model_id=model_id, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)

    raise last_exception


if __name__ == "__main__":
    response = invoke_bedrock_model(
        prompt="Explain quantum computing in simple terms.",
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    )
    print(response.text)
