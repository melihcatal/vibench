from __future__ import annotations

import os
from typing import Iterable, Iterator, Optional

from openai import OpenAI

from model_models import GenerationConfig, LLMRequest, LLMResponse, choose_model


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=key, base_url=base_url)
    return OpenAI(api_key=key)


def default_config(
    task: str, max_output_tokens: int = 512, temperature: float = 0.2
) -> GenerationConfig:
    return GenerationConfig(
        model=choose_model(task),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_p=0.95,
    )


def complete_text(request: LLMRequest, api_key: Optional[str] = None) -> LLMResponse:
    if request.config is None:
        request.config = default_config("chat")
    client = get_openai_client(api_key=api_key)
    response = client.chat.completions.create(
        model=request.config.model,
        messages=request.to_openai_messages(),
        temperature=request.config.temperature,
        max_completion_tokens=request.config.max_output_tokens,
        top_p=request.config.top_p,
    )
    text = response.choices[0].message.content or ""
    return LLMResponse(
        provider="openai", model=request.config.model, text=text, raw=response
    )


def stream_text(request: LLMRequest, api_key: Optional[str] = None) -> Iterator[str]:
    if request.config is None:
        request.config = default_config("stream")
    client = get_openai_client(api_key=api_key)
    stream = client.chat.completions.create(
        model=request.config.model,
        messages=request.to_openai_messages(),
        temperature=request.config.temperature,
        max_completion_tokens=request.config.max_output_tokens,
        top_p=request.config.top_p,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def collect_stream(chunks: Iterable[str]) -> str:
    return "".join(chunks)
