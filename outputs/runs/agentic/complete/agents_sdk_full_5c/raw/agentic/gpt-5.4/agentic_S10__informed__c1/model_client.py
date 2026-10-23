from __future__ import annotations

import os
from typing import Iterable, Iterator, Optional

from openai import OpenAI

from model_models import GenerationOptions, NormalizedLLMResult, normalize_chat_response

DEFAULT_FAST_MODEL = os.getenv("OPENAI_FAST_MODEL", "gpt-4o-mini")
DEFAULT_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1")
DEFAULT_JSON_MODEL = os.getenv("OPENAI_JSON_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class HostedModelClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL"),
        )

    def select_model_family(self, task: str) -> str:
        normalized = task.strip().lower()
        if normalized in {"json", "extract", "schema"}:
            return DEFAULT_JSON_MODEL
        if normalized in {"summary", "answer", "stream"}:
            return DEFAULT_FAST_MODEL
        if normalized in {"reasoning", "analysis"}:
            return DEFAULT_REASONING_MODEL
        return DEFAULT_FAST_MODEL

    def chat(self, messages: list[dict[str, str]], options: GenerationOptions) -> NormalizedLLMResult:
        response = self.client.chat.completions.create(messages=messages, **options.as_kwargs())
        return normalize_chat_response(response)

    def stream_chat(self, messages: list[dict[str, str]], options: GenerationOptions) -> Iterator[str]:
        stream = self.client.chat.completions.create(messages=messages, stream=True, **options.as_kwargs())
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                yield content

    def embed(self, texts: Iterable[str], model: Optional[str] = None) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=model or DEFAULT_EMBEDDING_MODEL,
            input=list(texts),
        )
        return [item.embedding for item in response.data]
