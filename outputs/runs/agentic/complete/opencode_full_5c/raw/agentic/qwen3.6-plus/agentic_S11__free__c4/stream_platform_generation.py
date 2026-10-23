from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import (
    PlatformMessage,
    PlatformRequest,
    StreamChunk,
    StreamedResponse,
    MessageRole,
    normalize_streamed_response,
)


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> StreamedResponse:
    messages: list[PlatformMessage] = []
    if system_prompt:
        messages.append(PlatformMessage(role=MessageRole.SYSTEM, content=system_prompt))
    messages.append(PlatformMessage(role=MessageRole.USER, content=prompt))

    request = PlatformRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    openai_client = client or create_openai_client(config)

    payload = request.to_openai_payload()

    stream = openai_client.chat.completions.create(**payload)

    chunks: list[StreamChunk] = []
    raw_response = None

    for chunk in stream:
        raw_response = chunk
        for choice in chunk.choices:
            delta_text = choice.delta.content or ""
            finish_reason = choice.finish_reason
            chunk_obj = StreamChunk(
                delta=delta_text,
                finish_reason=finish_reason,
                index=choice.index,
                raw_chunk=chunk,
            )
            chunks.append(chunk_obj)

    return normalize_streamed_response(chunks, raw_response)


def stream_platform_generation_with_callback(
    prompt: str,
    on_chunk: callable,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> StreamedResponse:
    messages: list[PlatformMessage] = []
    if system_prompt:
        messages.append(PlatformMessage(role=MessageRole.SYSTEM, content=system_prompt))
    messages.append(PlatformMessage(role=MessageRole.USER, content=prompt))

    request = PlatformRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    openai_client = client or create_openai_client(config)
    payload = request.to_openai_payload()
    stream = openai_client.chat.completions.create(**payload)

    chunks: list[StreamChunk] = []
    raw_response = None

    for chunk in stream:
        raw_response = chunk
        for choice in chunk.choices:
            delta_text = choice.delta.content or ""
            finish_reason = choice.finish_reason
            chunk_obj = StreamChunk(
                delta=delta_text,
                finish_reason=finish_reason,
                index=choice.index,
                raw_chunk=chunk,
            )
            chunks.append(chunk_obj)
            on_chunk(chunk_obj)

    return normalize_streamed_response(chunks, raw_response)


if __name__ == "__main__":

    def _print_chunk(c: StreamChunk) -> None:
        print(c.delta, end="", flush=True)

    result = stream_platform_generation_with_callback(
        prompt="Write a short poem about the ocean.",
        on_chunk=_print_chunk,
        model="gpt-4o",
    )
    print(f"\n\nTotal chunks: {len(result.chunks)}")
