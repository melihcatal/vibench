"""Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class.
Uses Azure-specific deployment-scoped invocation model: the model parameter
is the Azure OpenAI deployment name (e.g., 'gpt-4o', 'gpt-35-turbo').
"""

from __future__ import annotations

from typing import Optional

from openai import AzureOpenAI

from model_client import build_azure_openai_client, build_chat_payload
from model_models import (
    PlatformRequest,
    PlatformResponse,
    normalize_messages,
)


def invoke_platform_model(
    *,
    prompt: str,
    deployment_id: str,
    client: Optional[AzureOpenAI] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
) -> PlatformResponse:
    """Invoke an Azure OpenAI managed model through the deployment-scoped platform client.

    Sends a chat completion request to the specified Azure OpenAI deployment
    and returns a normalized PlatformResponse.

    The Azure OpenAI provider requires the model parameter to be the deployment
    name configured in the Azure resource (e.g., 'gpt-4o', 'gpt-4', 'gpt-35-turbo').

    Args:
        prompt: The user input text.
        deployment_id: Azure OpenAI deployment name (resource-scoped identifier).
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        system_prompt: Optional system prompt to prepend to the conversation.
        temperature: Sampling temperature (0.0 - 2.0).
        max_tokens: Maximum tokens to generate.
        top_p: Nucleus sampling parameter.
        frequency_penalty: Frequency penalty (-2.0 to 2.0).
        presence_penalty: Presence penalty (-2.0 to 2.0).

    Returns:
        PlatformResponse with content, usage, and Azure provider metadata.

    Raises:
        RuntimeError: If the Azure OpenAI client cannot be built or the invocation fails.
    """
    if client is None:
        client = build_azure_openai_client()

    messages = normalize_messages(prompt, system_prompt=system_prompt)

    payload = build_chat_payload(
        deployment=deployment_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=False,
    )

    try:
        response = client.chat.completions.create(**payload)
    except Exception as exc:
        raise RuntimeError(
            f"Azure OpenAI deployment '{deployment_id}' invocation failed: {exc}"
        ) from exc

    return PlatformResponse.from_azure_response(response)


def invoke_with_request_object(
    *,
    request: PlatformRequest,
    client: Optional[AzureOpenAI] = None,
) -> PlatformResponse:
    """Invoke an Azure OpenAI model using a pre-built PlatformRequest object.

    Args:
        request: PlatformRequest with all parameters set.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.

    Returns:
        PlatformResponse with content, usage, and Azure provider metadata.
    """
    if client is None:
        client = build_azure_openai_client()

    api_kwargs = request.to_api_kwargs()
    api_kwargs["stream"] = False

    try:
        response = client.chat.completions.create(**api_kwargs)
    except Exception as exc:
        raise RuntimeError(
            f"Azure OpenAI deployment '{request.deployment_id}' invocation failed: {exc}"
        ) from exc

    return PlatformResponse.from_azure_response(response)


def invoke_batch_conversations(
    *,
    conversations: list[list[dict[str, str]]],
    deployment_id: str,
    client: Optional[AzureOpenAI] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> list[PlatformResponse]:
    """Invoke an Azure OpenAI model for multiple independent conversations.

    Useful for batch processing scenarios where each conversation has its own
    message history.

    Args:
        conversations: List of message lists, each representing one conversation.
        deployment_id: Azure OpenAI deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate per conversation.

    Returns:
        List of PlatformResponse, one per conversation, in input order.
    """
    if client is None:
        client = build_azure_openai_client()

    results = []
    for messages in conversations:
        response = client.chat.completions.create(
            model=deployment_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        results.append(PlatformResponse.from_azure_response(response))

    return results
