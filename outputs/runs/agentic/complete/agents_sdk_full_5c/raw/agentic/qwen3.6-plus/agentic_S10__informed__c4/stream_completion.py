"""
Stream partial output tokens from a hosted LLM using Anthropic Messages API.
Provider: Anthropic (anthropic SDK, ANTHROPIC_API_KEY)
"""

from typing import Optional, Generator, Callable

import anthropic

from model_client import get_anthropic_client, build_messages_prompt
from model_models import LLMRequest


DEFAULT_STREAM_MODEL = "claude-3-5-sonnet-20241022"


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> Generator[str, None, None]:
    """
    Stream partial text tokens from Anthropic Claude.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system prompt.
        model_id: Anthropic model identifier.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Yields:
        Incremental text deltas as they are generated.
    """
    if model_id is None:
        model_id = DEFAULT_STREAM_MODEL

    messages = build_messages_prompt(user_prompt=prompt)

    client = get_anthropic_client()

    with client.messages.stream(
        model=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages,
        system=system_prompt or None,
    ) as stream:
        for text in stream.text_stream:
            yield text


def stream_completion_with_callback(
    prompt: str,
    callback: Callable[[str], None],
    system_prompt: Optional[str] = None,
    model_id: Optional[str] = None,
) -> str:
    """
    Stream completion and invoke a callback for each token chunk.

    Args:
        prompt: The user prompt.
        callback: Function called with each text chunk.
        system_prompt: Optional system prompt.
        model_id: Anthropic model identifier.

    Returns:
        The complete accumulated text.
    """
    full_text = ""
    for chunk in stream_completion(prompt, system_prompt, model_id):
        callback(chunk)
        full_text += chunk
    return full_text


def stream_to_list(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: str = DEFAULT_STREAM_MODEL,
) -> list:
    """
    Stream completion and return chunks as a list.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system prompt.
        model_id: Anthropic model identifier.

    Returns:
        List of text chunks from the stream.
    """
    return list(stream_completion(prompt, system_prompt, model_id))
