from __future__ import annotations

import json
import os
from typing import Any, Dict, Generator, Iterable, Optional

from openai import OpenAI

from model_models import ChatRequest, ChatResponse, normalize_text

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_messages(request: ChatRequest) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if request.system:
        messages.append({"role": "system", "content": request.system})
    if request.context:
        messages.append({"role": "user", "content": f"Context:\n{request.context}"})
    if request.user:
        messages.append({"role": "user", "content": request.user})
    return messages


def select_model_family(model_family: str) -> str:
    family = (model_family or "").lower()
    if family in {"reasoning", "analysis", "default"}:
        return os.getenv("OPENAI_REASONING_MODEL", DEFAULT_OPENAI_MODEL)
    if family in {"json", "structured", "extract"}:
        return os.getenv("OPENAI_JSON_MODEL", DEFAULT_OPENAI_MODEL)
    if family in {"summary", "summarize", "chat"}:
        return os.getenv("OPENAI_CHAT_MODEL", DEFAULT_OPENAI_MODEL)
    return os.getenv("OPENAI_FALLBACK_MODEL", DEFAULT_OPENAI_MODEL)


def complete_text(request: ChatRequest) -> ChatResponse:
    client = _client()
    model = select_model_family(request.model_family)
    completion = client.chat.completions.create(
        model=model,
        messages=build_messages(request),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        response_format=request.response_format,
    )
    text = normalize_text(completion.choices[0].message.content)
    return ChatResponse(text=text, raw=completion, model=model, usage=getattr(completion, "usage", {}) or {})


def complete_json(request: ChatRequest) -> Dict[str, Any]:
    result = complete_text(request)
    try:
        return json.loads(result.text)
    except json.JSONDecodeError:
        return {"raw_text": result.text}


def stream_text(request: ChatRequest) -> Generator[str, None, ChatResponse]:
    client = _client()
    model = select_model_family(request.model_family)
    stream = client.chat.completions.create(
        model=model,
        messages=build_messages(request),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    chunks: list[str] = []
    for event in stream:
        delta = getattr(event.choices[0].delta, "content", None)
        if delta:
            chunks.append(delta)
            yield delta
    return ChatResponse(text="".join(chunks), raw=stream, model=model)
