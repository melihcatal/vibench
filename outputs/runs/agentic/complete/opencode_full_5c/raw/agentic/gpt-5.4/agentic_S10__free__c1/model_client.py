from __future__ import annotations

import os
from typing import Iterable, Iterator, Optional

from openai import OpenAI

from model_models import ChatTurn, CompletionResult, normalize_messages, package_result


DEFAULT_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
DEFAULT_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1")
DEFAULT_MODERATION_MODEL = os.getenv(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def choose_model(task: str, override: Optional[str] = None) -> str:
    if override:
        return override
    if task in {"summarize", "extract", "answer", "stream", "translate"}:
        return DEFAULT_TEXT_MODEL
    if task == "safety":
        return DEFAULT_MODERATION_MODEL
    if task == "embed":
        return DEFAULT_EMBEDDING_MODEL
    if task == "spoken_brief":
        return DEFAULT_TTS_MODEL
    return DEFAULT_REASONING_MODEL


def generate_text(
    messages: Iterable[ChatTurn],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 500,
) -> CompletionResult:
    selected_model = choose_model("summarize", model)
    response = get_client().responses.create(
        model=selected_model,
        input=normalize_messages(messages),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    return package_result(
        response.output_text, selected_model, getattr(response, "usage", None)
    )


def stream_text(
    messages: Iterable[ChatTurn],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 500,
) -> Iterator[str]:
    selected_model = choose_model("stream", model)
    with get_client().responses.stream(
        model=selected_model,
        input=normalize_messages(messages),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
