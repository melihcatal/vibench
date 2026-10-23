from __future__ import annotations

from typing import Generator, Optional

from model_client import stream_llm
from model_models import LLMRequest, StreamChunk, normalize_prompt

STREAM_MODEL = "gpt-4o"
STREAM_SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Provide clear and accurate responses."
)


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Generator[StreamChunk, None, None]:
    normalized = normalize_prompt(prompt)
    request = LLMRequest(
        model=model or STREAM_MODEL,
        prompt=normalized,
        system_prompt=system_prompt or STREAM_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    yield from stream_llm(request, api_key=api_key, base_url=base_url)


def stream_completion_to_string(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    full_text = []
    for chunk in stream_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
        api_key=api_key,
        base_url=base_url,
    ):
        full_text.append(chunk.delta)
    return "".join(full_text)


def stream_completion_with_callback(
    prompt: str,
    on_chunk: callable,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    full_text = []
    for chunk in stream_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model=model,
        api_key=api_key,
        base_url=base_url,
    ):
        on_chunk(chunk)
        full_text.append(chunk.delta)
    return "".join(full_text)


if __name__ == "__main__":
    import os

    for chunk in stream_completion(
        prompt="Write a short poem about technology.",
        api_key=os.environ.get("OPENAI_API_KEY"),
    ):
        print(chunk.delta, end="", flush=True)
    print()
