"""
[SAME-SCENARIO] Streams output from a managed model platform while preserving
provider response objects from Azure OpenAI.

Uses the Azure OpenAI SDK streaming API to yield generation chunks as they arrive,
preserving the raw Azure OpenAI response objects for downstream processing.
"""

from __future__ import annotations

from typing import Iterator, Optional

from openai import AzureOpenAI

from model_models import PlatformModelRequest, StreamingChunk, PlatformModelResponse
from model_client import (
    get_azure_openai_client,
    build_messages,
    extract_token_usage,
)
from select_platform_resource import resolve_deployment_for_request


def stream_platform_generation(
    request: PlatformModelRequest,
    client: Optional[AzureOpenAI] = None,
) -> Iterator[StreamingChunk]:
    """
    Stream output from an Azure OpenAI managed model deployment.

    Uses the Azure OpenAI chat.completions.create streaming interface to yield
    individual text chunks as they are generated, while preserving the raw
    Azure OpenAI response objects in each StreamingChunk.

    Args:
        request: PlatformModelRequest with deployment and content configuration.
        client: Optional pre-configured AzureOpenAI client.

    Yields:
        StreamingChunk objects containing text deltas and raw Azure OpenAI
        stream response data.
    """
    if client is None:
        client = get_azure_openai_client()

    resolved_deployment, _ = resolve_deployment_for_request(request, client)

    messages = build_messages(request.system_prompt, request.user_content)

    stream_kwargs: dict = {
        "model": resolved_deployment,
        "messages": messages,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "stream": True,
    }

    if request.max_tokens is not None:
        stream_kwargs["max_tokens"] = request.max_tokens

    if request.stop is not None:
        stream_kwargs["stop"] = request.stop

    if request.extra_body is not None:
        stream_kwargs["extra_body"] = request.extra_body

    stream = client.chat.completions.create(**stream_kwargs)

    for chunk in stream:
        if chunk.choices and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            delta = choice.delta
            content_delta = getattr(delta, "content", None) or ""

            streaming_chunk = StreamingChunk(
                content=content_delta,
                finish_reason=choice.finish_reason,
                index=choice.index,
                raw_delta=chunk,
            )
            yield streaming_chunk


def stream_and_collect(
    request: PlatformModelRequest,
    client: Optional[AzureOpenAI] = None,
) -> PlatformModelResponse:
    """
    Stream Azure OpenAI output and collect the full response with metadata.

    Streams the generation, accumulates all text chunks, and returns a
    complete PlatformModelResponse with the combined content and metadata.

    Args:
        request: PlatformModelRequest with deployment and content configuration.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        PlatformModelResponse with fully streamed content and provider metadata.
    """
    accumulated_content = ""
    finish_reason = None
    model_id = None
    last_raw_chunk = None

    for chunk in stream_platform_generation(request, client):
        accumulated_content += chunk.content
        if chunk.finish_reason is not None:
            finish_reason = chunk.finish_reason
        if chunk.raw_delta is not None:
            model_id = getattr(chunk.raw_delta, "model", request.deployment_name)
            last_raw_chunk = chunk.raw_delta

    usage = {}
    if last_raw_chunk is not None:
        usage = extract_token_usage(last_raw_chunk)

    return PlatformModelResponse(
        content=accumulated_content,
        model_id=model_id or request.deployment_name,
        deployment_name=request.deployment_name,
        finish_reason=finish_reason,
        usage=usage,
        raw_response=last_raw_chunk,
    )


def stream_with_metadata_preservation(
    request: PlatformModelRequest,
    client: Optional[AzureOpenAI] = None,
) -> Iterator[tuple[StreamingChunk, Optional[dict]]]:
    """
    Stream Azure OpenAI output while attaching per-chunk metadata.

    Yields tuples of (StreamingChunk, metadata_dict) where metadata contains
    Azure OpenAI-specific information like request ID and model.

    Args:
        request: PlatformModelRequest with deployment and content configuration.
        client: Optional pre-configured AzureOpenAI client.

    Yields:
        Tuples of (StreamingChunk, metadata_dict) for each streamed chunk.
    """
    if client is None:
        client = get_azure_openai_client()

    resolved_deployment, _ = resolve_deployment_for_request(request, client)
    messages = build_messages(request.system_prompt, request.user_content)

    stream_kwargs: dict = {
        "model": resolved_deployment,
        "messages": messages,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "stream": True,
    }

    if request.max_tokens is not None:
        stream_kwargs["max_tokens"] = request.max_tokens

    stream = client.chat.completions.create(**stream_kwargs)

    for chunk in stream:
        chunk_metadata = {
            "azure_model_id": getattr(chunk, "model", resolved_deployment),
            "azure_request_id": getattr(chunk, "id", None),
            "azure_created": getattr(chunk, "created", None),
            "deployment_name": resolved_deployment,
        }

        if chunk.choices and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            delta = choice.delta
            content_delta = getattr(delta, "content", None) or ""

            streaming_chunk = StreamingChunk(
                content=content_delta,
                finish_reason=choice.finish_reason,
                index=choice.index,
                raw_delta=chunk,
            )
            yield streaming_chunk, chunk_metadata
