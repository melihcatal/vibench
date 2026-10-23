"""Streams output from a managed model platform while preserving provider response objects.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class, with stream=True parameter.
Uses concrete Azure OpenAI deployment-scoped model invocation with streaming.
"""

from __future__ import annotations

from typing import Optional, Iterator, Any

from openai import AzureOpenAI

from model_client import build_azure_openai_client, build_chat_payload
from model_models import (
    PlatformRequest,
    PlatformResponse,
    StreamingChunk,
    normalize_messages,
)


def stream_platform_generation(
    *,
    prompt: str,
    deployment_id: str,
    client: Optional[AzureOpenAI] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 1.0,
) -> Iterator[StreamingChunk]:
    """Stream output from an Azure OpenAI deployment while preserving provider objects.

    Yields normalized StreamingChunk objects for each token increment. The underlying
    Azure OpenAI API response stream (openai.Stream) is preserved for access to
    raw provider metadata such as request_id, model, and system_fingerprint.

    Args:
        prompt: The user input text.
        deployment_id: Azure OpenAI deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        system_prompt: Optional system prompt.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.
        top_p: Nucleus sampling parameter.

    Yields:
        StreamingChunk for each received delta.
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
        stream=True,
    )

    # The Azure OpenAI provider returns an openai.Stream object
    stream = client.chat.completions.create(**payload)

    for chunk in stream:
        # chunk is the raw Azure OpenAI provider response object
        yield StreamingChunk.from_azure_chunk(chunk)


def stream_with_full_response(
    *,
    prompt: str,
    deployment_id: str,
    client: Optional[AzureOpenAI] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> tuple[str, Any, PlatformResponse]:
    """Stream output and accumulate into a full PlatformResponse with raw provider object.

    Returns the accumulated text, the raw Azure OpenAI stream object (for inspection
    of provider-specific metadata), and a normalized PlatformResponse built from
    the last chunk.

    Args:
        prompt: The user input text.
        deployment_id: Azure OpenAI deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        system_prompt: Optional system prompt.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Returns:
        Tuple of (accumulated_text, raw_stream, PlatformResponse).
    """
    if client is None:
        client = build_azure_openai_client()

    messages = normalize_messages(prompt, system_prompt=system_prompt)

    payload = build_chat_payload(
        deployment=deployment_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    raw_stream = client.chat.completions.create(**payload)

    accumulated = []
    last_chunk = None

    for chunk in raw_stream:
        last_chunk = chunk
        sc = StreamingChunk.from_azure_chunk(chunk)
        if sc.content:
            accumulated.append(sc.content)

    full_text = "".join(accumulated)

    # Build a synthetic PlatformResponse from the last chunk
    response_obj = PlatformResponse(
        content=full_text,
        model_id=getattr(last_chunk, "model", deployment_id) if last_chunk else deployment_id,
        finish_reason=(
            last_chunk.choices[0].finish_reason
            if last_chunk and last_chunk.choices
            else "unknown"
        ),
    )

    return full_text, raw_stream, response_obj


def stream_with_request_object(
    *,
    request: PlatformRequest,
    client: Optional[AzureOpenAI] = None,
) -> Iterator[StreamingChunk]:
    """Stream output using a pre-built PlatformRequest.

    Args:
        request: PlatformRequest with all parameters set (must have stream=True).
        client: Pre-built AzureOpenAI client. Built automatically if not provided.

    Yields:
        StreamingChunk for each received delta.
    """
    if client is None:
        client = build_azure_openai_client()

    api_kwargs = request.to_api_kwargs()
    api_kwargs["stream"] = True

    stream = client.chat.completions.create(**api_kwargs)

    for chunk in stream:
        yield StreamingChunk.from_azure_chunk(chunk)
