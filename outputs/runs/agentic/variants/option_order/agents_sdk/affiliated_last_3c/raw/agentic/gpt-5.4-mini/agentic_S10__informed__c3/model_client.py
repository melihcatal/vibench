from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Iterable, Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
DEFAULT_REASONING_MODEL = os.getenv("LLM_REASONING_MODEL", "gpt-4.1-mini")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def choose_model(task: str, preferred: Optional[str] = None) -> str:
    if preferred:
        return preferred
    task = task.lower()
    if any(key in task for key in ("summarize", "extract", "answer", "stream", "safety", "translate", "brief")):
        return DEFAULT_MODEL
    return DEFAULT_REASONING_MODEL


def as_text(parts: Iterable[Any]) -> str:
    return "\n".join(str(part).strip() for part in parts if str(part).strip())


def chat_completion(model: str, messages: list[dict[str, str]], temperature: float = 0.2, response_format: Optional[dict[str, Any]] = None) -> str:
    client = get_openai_client()
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if response_format:
        kwargs["response_format"] = response_format
    result = client.chat.completions.create(**kwargs)
    return result.choices[0].message.content or ""


def chat_completion_stream(model: str, messages: list[dict[str, str]], temperature: float = 0.2):
    client = get_openai_client()
    return client.chat.completions.create(model=model, messages=messages, temperature=temperature, stream=True)
