"""
[SAME-SCENARIO] Streams output from Amazon Bedrock managed model platform
while preserving provider response objects.

Provider: Amazon Bedrock
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
from typing import Generator, Optional

from model_client import get_bedrock_runtime_client, resolve_model_id
from model_models import (
    StreamedChunk,
    PlatformResponse,
    parse_stream_event,
    collect_streamed_text,
    build_user_message,
)


def stream_model(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> Generator[StreamedChunk, None, None]:
    """Stream tokens from an Amazon Bedrock model using ConverseStream API.

    Provider signals: boto3 bedrock-runtime converse_stream, Bedrock streaming
    event types (messageStart, contentBlockDelta, messageStop, metadata),
    Bedrock model identifiers.
    """
    client = get_bedrock_runtime_client(region_name=region)
    resolved_model = resolve_model_id(model_id) if model_id else "anthropic.claude-3-5-sonnet-20241022-v2:0"

    payload = {
        "modelId": resolved_model,
        "messages": [build_user_message(prompt)],
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
        },
    }
    if system_prompt:
        payload["system"] = [{"text": system_prompt}]

    response = client.converse_stream(**payload)

    # Preserve the raw provider response for downstream access
    stream = response.get("stream", [])
    for event in stream:
        chunk = parse_stream_event(event)
        if chunk is not None:
            yield chunk


def stream_and_collect(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> dict:
    """Stream tokens and collect the final output with full provider metadata.

    Returns a dict with:
    - output_text: the full streamed text
    - chunks: list of all StreamedChunk objects
    - stop_reason: from the final messageStop event
    - usage: token usage from the metadata event

    Provider signals: Amazon Bedrock ConverseStream response handling.
    """
    chunks: list[StreamedChunk] = []
    stop_reason = None
    usage = {}

    for chunk in stream_model(
        prompt=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        region=region,
    ):
        chunks.append(chunk)
        if chunk.chunk_type == "messageStop":
            stop_reason = chunk.stop_reason
        if chunk.chunk_type == "metadata":
            usage = chunk.usage or {}

    output_text = collect_streamed_text(chunks)

    return {
        "output_text": output_text,
        "chunks": chunks,
        "stop_reason": stop_reason,
        "usage": usage,
        "provider": "amazon-bedrock",
    }


def stream_with_callback(
    prompt: str,
    on_chunk: callable,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    region: Optional[str] = None,
) -> PlatformResponse:
    """Stream tokens and invoke a callback on each content block delta.

    Provider signals: Bedrock ConverseStream with per-chunk callback processing.
    """
    accumulated_text = []
    stop_reason = None

    for chunk in stream_model(
        prompt=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        region=region,
    ):
        if chunk.chunk_type == "contentBlockDelta" and chunk.text:
            accumulated_text.append(chunk.text)
            on_chunk(chunk.text, chunk)
        if chunk.chunk_type == "messageStop":
            stop_reason = chunk.stop_reason

    return PlatformResponse(
        output_text="".join(accumulated_text),
        stop_reason=stop_reason,
    )
