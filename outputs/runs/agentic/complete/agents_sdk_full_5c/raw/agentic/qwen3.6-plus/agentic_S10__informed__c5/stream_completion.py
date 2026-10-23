"""
Same-scenario: Stream partial output tokens from a hosted LLM.

Provider: OpenAI GPT via OpenAI API
SDK: openai
Auth: OPENAI_API_KEY
Model: gpt-4o
"""

from typing import Optional, Generator, Callable

from model_client import (
    create_openai_client,
    create_async_openai_client,
    build_messages,
    get_default_model,
    normalize_stream_delta,
)
from model_models import CompletionRequest, StreamChunk


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    on_chunk: Optional[Callable[[StreamChunk], None]] = None,
) -> str:
    """
    Stream partial tokens from OpenAI GPT-4o and return the accumulated text.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system message.
        model: The OpenAI model identifier. Defaults to gpt-4o.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.
        on_chunk: Optional callback invoked for each streamed chunk.

    Returns:
        The fully accumulated response text.
    """
    client = create_openai_client()

    messages = build_messages(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    request = CompletionRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model or get_default_model(),
        temperature=temperature,
        max_tokens=max_tokens,
    )

    openai_kwargs = request.to_openai_kwargs(messages)
    openai_kwargs["stream"] = True

    accumulated = ""
    stream = client.chat.completions.create(**openai_kwargs)

    for chunk in stream:
        delta_content = normalize_stream_delta(chunk.choices[0].delta if chunk.choices else None)
        if delta_content:
            accumulated += delta_content
            stream_chunk = StreamChunk(
                content=delta_content,
                accumulated_text=accumulated,
            )
            if on_chunk:
                on_chunk(stream_chunk)

    return accumulated


async def async_stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    on_chunk: Optional[Callable[[StreamChunk], None]] = None,
) -> str:
    """
    Async version of stream_completion using AsyncOpenAI client.
    """
    client = create_async_openai_client()

    messages = build_messages(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    request = CompletionRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model or get_default_model(),
        temperature=temperature,
        max_tokens=max_tokens,
    )

    openai_kwargs = request.to_openai_kwargs(messages)
    openai_kwargs["stream"] = True

    accumulated = ""
    stream = await client.chat.completions.create(**openai_kwargs)

    async for chunk in stream:
        delta_content = normalize_stream_delta(chunk.choices[0].delta if chunk.choices else None)
        if delta_content:
            accumulated += delta_content
            stream_chunk = StreamChunk(
                content=delta_content,
                accumulated_text=accumulated,
            )
            if on_chunk:
                on_chunk(stream_chunk)

    return accumulated
