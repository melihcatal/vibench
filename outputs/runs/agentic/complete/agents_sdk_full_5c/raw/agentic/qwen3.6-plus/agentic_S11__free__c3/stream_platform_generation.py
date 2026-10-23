"""Streams output from a managed Anthropic model platform while preserving provider response objects.

Uses the Anthropic Messages API with streaming to generate output from
claude-3-5-sonnet-20241022, preserving Anthropic-specific response
objects and streaming events throughout the generation process.
"""

from typing import Dict, Any, Optional, Iterator, List

import anthropic
from anthropic import Anthropic, Stream
from anthropic.types import MessageStreamEvent

from model_client import load_platform_config, get_anthropic_client
from model_models import (
    PlatformInvocationRequest,
    StreamingChunk,
    build_platform_request,
)


ANTHROPIC_STREAMING_MODEL = "claude-3-5-sonnet-20241022"


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Iterator[StreamingChunk]:
    """Stream output from the Anthropic managed model platform.

    Uses the Anthropic Messages API with streaming enabled to yield
    text deltas as they are generated from claude-3-5-sonnet-20241022.
    Each StreamingChunk preserves the raw Anthropic provider event object.

    Args:
        prompt: User input text to send to the model.
        system_prompt: Optional system-level instructions.
        model: Override the default Anthropic model identifier.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature (0.0 to 1.0).
        provider_config: Optional pre-loaded Anthropic configuration.

    Yields:
        StreamingChunk objects with text deltas and raw Anthropic events.
    """
    if provider_config is None:
        provider_config = load_platform_config("anthropic")

    model_id = model or provider_config.get("default_model", ANTHROPIC_STREAMING_MODEL)

    client = get_anthropic_client(provider_config)

    request = build_platform_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    system, messages = request.to_anthropic_messages()

    stream = client.messages.create(
        model=model_id,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        system=system,
        messages=messages,
        stream=True,
    )

    for event in stream:
        chunk = StreamingChunk(
            text="",
            index=0,
            raw_chunk=event,
        )

        if event.type == "content_block_delta":
            if hasattr(event.delta, "text") and event.delta.text:
                chunk.text = event.delta.text
            yield chunk
        elif event.type == "message_delta":
            if hasattr(event.delta, "stop_reason") and event.delta.stop_reason:
                chunk.finish_reason = event.delta.stop_reason
            yield chunk
        elif event.type == "content_block_stop":
            chunk.finish_reason = "content_block_end"
            yield chunk


def stream_with_full_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Stream generation and return the full accumulated result with Anthropic metadata.

    Streams all chunks from the Anthropic platform and accumulates the
    complete response, returning text along with the final message metadata.

    Args:
        prompt: User input text.
        system_prompt: Optional system prompt.
        model: Anthropic model override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary with accumulated text, stop_reason, model, and raw response.
    """
    if provider_config is None:
        provider_config = load_platform_config("anthropic")

    model_id = model or provider_config.get("default_model", ANTHROPIC_STREAMING_MODEL)
    client = get_anthropic_client(provider_config)

    request = build_platform_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model_id,
    )

    system, messages = request.to_anthropic_messages()

    accumulated_text = ""
    final_message = None

    with client.messages.stream(
        model=model_id,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        system=system,
        messages=messages,
    ) as stream:
        for text_delta in stream.text_stream:
            accumulated_text += text_delta

        final_message = stream.get_final_message()

    result: Dict[str, Any] = {
        "text": accumulated_text,
        "model": model_id,
        "provider": "anthropic",
    }

    if final_message:
        result["response_id"] = getattr(final_message, "id", None)
        result["stop_reason"] = getattr(final_message, "stop_reason", None)
        result["role"] = getattr(final_message, "role", None)
        if hasattr(final_message, "usage"):
            result["usage"] = {
                "input_tokens": getattr(final_message.usage, "input_tokens", None),
                "output_tokens": getattr(final_message.usage, "output_tokens", None),
            }
        result["raw_response"] = final_message

    return result
