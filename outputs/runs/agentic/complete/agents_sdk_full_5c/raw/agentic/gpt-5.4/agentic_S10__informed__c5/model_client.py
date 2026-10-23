from __future__ import annotations

import os
from typing import Iterable, Optional

from openai import OpenAI

from model_models import InferenceRequest, InferenceResponse


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def choose_chat_model(task: str, preferred_model: Optional[str] = None) -> str:
    if preferred_model:
        return preferred_model
    task = task.lower()
    if "json" in task or "extract" in task:
        return os.getenv("OPENAI_JSON_MODEL", DEFAULT_CHAT_MODEL)
    if "summarize" in task or "answer" in task or "stream" in task:
        return DEFAULT_CHAT_MODEL
    return DEFAULT_CHAT_MODEL


def complete_text(request: InferenceRequest) -> InferenceResponse:
    client = get_openai_client()
    model = choose_chat_model(request.user_prompt, request.model)
    response = client.chat.completions.create(
        model=model,
        messages=request.to_messages(),
        temperature=request.temperature if request.temperature is not None else DEFAULT_TEMPERATURE,
        max_tokens=request.max_tokens,
    )
    choice = response.choices[0]
    usage = response.usage.model_dump() if response.usage else {}
    return InferenceResponse(
        text=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason,
        usage=usage,
    )


def stream_text(request: InferenceRequest) -> Iterable[str]:
    client = get_openai_client()
    model = choose_chat_model("stream", request.model)
    stream = client.chat.completions.create(
        model=model,
        messages=request.to_messages(),
        temperature=request.temperature if request.temperature is not None else DEFAULT_TEMPERATURE,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
