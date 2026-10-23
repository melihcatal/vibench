"""
Stream partial output tokens from a hosted LLM.
Provider: OpenAI - https://platform.openai.com
Model: gpt-3.5-turbo (openai-gpt35-turbo family)
"""

from typing import Optional, Iterator, Callable
from model_client import get_openai_client, get_async_openai_client, resolve_model_family, DEFAULT_STREAM_MODEL
from model_models import (
    LLMRequest,
    LLMResponse,
    StreamChunk,
    normalize_system_user_messages,
    chunk_stream_from_openai,
)


STREAM_SYSTEM_PROMPT = (
    "You are a helpful assistant. Provide clear, well-structured responses."
)


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = DEFAULT_STREAM_MODEL,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Iterator[StreamChunk]:
    """
    Stream partial tokens from the OpenAI gpt-3.5-turbo model at api.openai.com.

    Yields StreamChunk objects as tokens are generated, enabling real-time
    display and processing of LLM output.

    Args:
        prompt: The user prompt to send.
        system_prompt: Optional system prompt to set assistant behavior.
        model: OpenAI model identifier (default: gpt-3.5-turbo).
        temperature: Sampling temperature.
        max_tokens: Maximum number of tokens to generate.
        api_key: Optional override for OPENAI_API_KEY.
        base_url: Optional override for OpenAI API endpoint.

    Yields:
        StreamChunk objects containing partial text and finish_reason.
    """
    sys_prompt = system_prompt or STREAM_SYSTEM_PROMPT
    messages = normalize_system_user_messages(sys_prompt, prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()

    openai_stream = client.chat.completions.create(**openai_kwargs)

    for chunk in chunk_stream_from_openai(openai_stream):
        yield chunk


def stream_completion_with_callback(
    prompt: str,
    on_token: Callable[[str], None],
    system_prompt: Optional[str] = None,
    model: str = DEFAULT_STREAM_MODEL,
    temperature: float = 0.7,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """
    Stream from OpenAI gpt-3.5-turbo and call a callback for each token.

    Args:
        prompt: The user prompt.
        on_token: Callback invoked with each token string as it arrives.
        system_prompt: Optional system instructions.
        model: OpenAI model identifier.
        temperature: Sampling temperature.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        The complete accumulated text from the stream.
    """
    full_text = []

    for chunk in stream_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        api_key=api_key,
        base_url=base_url,
    ):
        if chunk.text:
            full_text.append(chunk.text)
            on_token(chunk.text)

    return "".join(full_text)


async def async_stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = DEFAULT_STREAM_MODEL,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Iterator[StreamChunk]:
    """
    Asynchronously stream tokens from the OpenAI gpt-3.5-turbo model.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system prompt.
        model: OpenAI model identifier.
        temperature: Sampling temperature.
        max_tokens: Maximum output tokens.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Yields:
        StreamChunk objects as they arrive from the OpenAI streaming API.
    """
    sys_prompt = system_prompt or STREAM_SYSTEM_PROMPT
    messages = normalize_system_user_messages(sys_prompt, prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    client = get_async_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()

    stream = await client.chat.completions.create(**openai_kwargs)
    async for chunk in stream:
        for choice in chunk.choices:
            delta = choice.delta
            text = delta.content if delta and delta.content else ""
            finish = choice.finish_reason
            if text or finish:
                yield StreamChunk(text=text, finish_reason=finish, raw_chunk=chunk)


if __name__ == "__main__":
    import time

    print(f"Streaming from model: {DEFAULT_STREAM_MODEL}")
    print(f"Model family: {resolve_model_family(DEFAULT_STREAM_MODEL)}")
    print("Response: ", end="", flush=True)

    for chunk in stream_completion("Write a haiku about programming in Python."):
        if chunk.text:
            print(chunk.text, end="", flush=True)
        if chunk.finish_reason:
            print(f"\n\nFinished with: {chunk.finish_reason}")
