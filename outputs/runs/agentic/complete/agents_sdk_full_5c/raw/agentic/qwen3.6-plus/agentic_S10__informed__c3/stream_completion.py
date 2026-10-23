"""
Stream partial output tokens from a Mistral AI hosted LLM.

Provider: Mistral AI Chat API
SDK: mistralai
Auth: MISTRAL_API_KEY
"""

from __future__ import annotations

from typing import Iterator, Optional

from model_client import build_request, create_mistral_client, execute_chat_stream
from model_models import (
    StreamedChunk,
    LLMRequest,
)


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> Iterator[StreamedChunk]:
    """Stream partial output tokens from a Mistral AI model.

    Args:
        prompt: The user prompt / message to send.
        system_prompt: Optional system-level instruction.
        model: Optional concrete Mistral model identifier (e.g., 'mistral-medium-latest').
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.

    Yields:
        StreamedChunk instances containing each delta token.
    """
    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    yield from execute_chat_stream(request)


def stream_completion_with_client(
    prompt: str,
    client,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> Iterator[StreamedChunk]:
    """Stream partial tokens using a pre-created Mistral client.

    Args:
        prompt: The user prompt / message to send.
        client: An initialized mistralai.Mistral client.
        system_prompt: Optional system-level instruction.
        model: Optional concrete Mistral model identifier.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.

    Yields:
        StreamedChunk instances containing each delta token.
    """
    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    yield from execute_chat_stream(request, client=client)


def stream_completion_to_string(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """Stream partial tokens and accumulate the full response string.

    Args:
        prompt: The user prompt / message to send.
        system_prompt: Optional system-level instruction.
        model: Optional concrete Mistral model identifier.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.

    Returns:
        The fully accumulated response string.
    """
    chunks: list[str] = []
    for chunk in stream_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    ):
        chunks.append(chunk.delta)
    return "".join(chunks)
