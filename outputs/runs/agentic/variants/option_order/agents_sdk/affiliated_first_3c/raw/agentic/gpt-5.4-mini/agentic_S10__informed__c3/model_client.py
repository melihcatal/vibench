from __future__ import annotations

import os
from typing import Iterable, Iterator, List, Optional

from openai import OpenAI

from model_models import ChatMessage, LLMRequest, LLMResponse, StreamingChunk

DEFAULT_MODEL_FAMILY = os.getenv("OPENAI_MODEL_FAMILY", "gpt-4o-mini")
DEFAULT_API_KEY_VAR = "OPENAI_API_KEY"


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv(DEFAULT_API_KEY_VAR))


def build_messages(system: Optional[str], user_content: str) -> List[dict]:
    messages: List[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user_content})
    return messages


def normalize_request(model_family: str, messages: Iterable[ChatMessage], temperature: float = 0.2, max_tokens: int = 512) -> LLMRequest:
    return LLMRequest(model_family=model_family or DEFAULT_MODEL_FAMILY, messages=list(messages), temperature=temperature, max_tokens=max_tokens)


def chat_completion(request: LLMRequest) -> LLMResponse:
    client = get_openai_client()
    resp = client.chat.completions.create(
        model=request.model_family,
        messages=[{"role": m.role, "content": m.content} for m in request.messages],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
    )
    text = resp.choices[0].message.content or ""
    return LLMResponse(text=text, model=resp.model or request.model_family, usage=dict(resp.usage or {}), raw=resp)


def stream_chat_completion(request: LLMRequest) -> Iterator[StreamingChunk]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=request.model_family,
        messages=[{"role": m.role, "content": m.content} for m in request.messages],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stream=True,
    )
    for event in stream:
        delta = event.choices[0].delta.content if event.choices else None
        if delta:
            yield StreamingChunk(text=delta, done=False, raw=event)
    yield StreamingChunk(text="", done=True, raw=None)
