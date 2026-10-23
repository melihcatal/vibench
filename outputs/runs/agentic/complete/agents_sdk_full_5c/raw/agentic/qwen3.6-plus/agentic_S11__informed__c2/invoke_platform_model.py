"""
[SAME-SCENARIO] Invokes a provider-managed model through Amazon Bedrock's
Converse API (project-, deployment-, or inference-profile-scoped platform client).

Provider: Amazon Bedrock
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
from typing import Optional

from model_client import get_bedrock_runtime_client, resolve_model_id
from model_models import (
    PlatformRequest,
    PlatformResponse,
    build_user_message,
)


def invoke_model(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> PlatformResponse:
    """Invoke an Amazon Bedrock model using the Converse API.

    Provider signals: boto3 bedrock-runtime converse, Bedrock modelId format
    (e.g., anthropic.claude-3-5-sonnet-20241022-v2:0), AWS credentials.
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

    response = client.converse(**payload)

    return PlatformResponse.from_bedrock_response(response)


def invoke_with_history(
    messages: list[dict],
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> PlatformResponse:
    """Invoke an Amazon Bedrock model with conversation history.

    Provider signals: boto3 bedrock-runtime converse API, Bedrock message format
    with role/content structure specific to Amazon Bedrock.
    """
    client = get_bedrock_runtime_client(region_name=region)
    resolved_model = resolve_model_id(model_id) if model_id else "anthropic.claude-3-5-sonnet-20241022-v2:0"

    payload = {
        "modelId": resolved_model,
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
        },
    }
    if system_prompt:
        payload["system"] = [{"text": system_prompt}]

    response = client.converse(**payload)
    return PlatformResponse.from_bedrock_response(response)


def invoke_with_guardrails(
    prompt: str,
    guardrail_id: str,
    guardrail_version: str = "DRAFT",
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> PlatformResponse:
    """Invoke an Amazon Bedrock model with Bedrock Guardrails enabled.

    Provider signals: boto3 bedrock-runtime converse with `guardConfig`
    parameter (Bedrock Guardrails feature).
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
    payload["guardConfig"] = {
        "guardrailIdentifier": guardrail_id,
        "guardrailVersion": guardrail_version,
    }

    response = client.converse(**payload)
    return PlatformResponse.from_bedrock_response(response)


def run_platform_workflow(
    task: str,
    context: Optional[str] = None,
    model_id: Optional[str] = None,
    region: Optional[str] = None,
) -> str:
    """End-to-end: select resource, invoke model, return output text.

    Uses Amazon Bedrock as the managed model platform provider.
    """
    from select_platform_resource import select_resource

    resource = select_resource(task=task, region=region, prefer_model=model_id)
    resolved_model = resource["model_id"]

    full_prompt = task
    if context:
        full_prompt = f"Context: {context}\n\nTask: {task}"

    response = invoke_model(
        prompt=full_prompt,
        model_id=resolved_model,
        region=region,
    )
    return response.output_text
