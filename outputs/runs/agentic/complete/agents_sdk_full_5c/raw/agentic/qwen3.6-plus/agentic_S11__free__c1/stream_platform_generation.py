"""Stream output from a managed OpenAI model platform while preserving provider response objects.

Uses openai.Stream[ChatCompletionChunk] to yield tokens as they arrive,
accumulating chunks so that full provider response objects are available
after streaming completes.
"""

from __future__ import annotations

import os
from typing import Iterator, List, Optional, Tuple

from openai import OpenAI
from openai.types.chat import ChatCompletionChunk

from model_client import create_openai_client, resolve_deployment_model, with_retry
from model_models import PlatformModelRequest, PlatformModelResponse


def stream_platform_generation(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
) -> Iterator[Tuple[str, bool]]:
    """Stream output from an OpenAI managed model, yielding (token, is_finished) pairs.

    Preserves full ChatCompletionChunk objects so the caller can inspect
    provider-specific metadata during streaming.

    Yields:
        (token_text, is_finished) where is_finished is True on the final yield.
    """
    resolved_client = client or create_openai_client()
    payload = request.to_openai_payload()
    payload["stream"] = True
    # OpenAI requires stream_options={"include_usage": True} for usage in chunks
    payload["stream_options"] = {"include_usage": True}

    def _call():
        return resolved_client.chat.completions.create(**payload)

    stream = with_retry(_call)

    accumulated: List[ChatCompletionChunk] = []

    for chunk in stream:
        accumulated.append(chunk)
        token_text = ""
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                token_text = delta.content
        is_finished = chunk.choices and chunk.choices[0].finish_reason is not None
        if is_finished or token_text:
            yield token_text, is_finished

    # Store accumulated chunks on the stream object for later access
    stream._accumulated_chunks = accumulated  # type: ignore[attr-defined]


def stream_and_collect(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
) -> PlatformModelResponse:
    """Stream from OpenAI and return a fully accumulated PlatformModelResponse.

    Consumes the entire stream, collects all ChatCompletionChunk objects,
    and builds a normalized response.
    """
    resolved_client = client or create_openai_client()
    payload = request.to_openai_payload()
    payload["stream"] = True
    payload["stream_options"] = {"include_usage": True}

    def _call():
        return resolved_client.chat.completions.create(**payload)

    stream = with_retry(_call)
    chunks: List[ChatCompletionChunk] = []

    for chunk in stream:
        chunks.append(chunk)

    return PlatformModelResponse.from_openai_chunks(chunks)
