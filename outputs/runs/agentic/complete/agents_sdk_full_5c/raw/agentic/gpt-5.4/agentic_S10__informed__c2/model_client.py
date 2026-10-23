from __future__ import annotations

import os
from typing import Iterable, Optional

from openai import OpenAI

from model_models import ChatMessage, LLMRequest, LLMResponse

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class OpenAIModelClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or DEFAULT_OPENAI_MODEL
        self.client = OpenAI(api_key=self.api_key)

    def complete(self, request: LLMRequest) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=request.model or self.model,
            messages=request.normalized_messages(),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )
        content = response.choices[0].message.content or ""
        return LLMResponse(model=response.model, content=content, raw=response)

    def stream(self, request: LLMRequest) -> Iterable[str]:
        response = self.client.chat.completions.create(
            model=request.model or self.model,
            messages=request.normalized_messages(),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )
        for chunk in response:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


def build_text_request(
    system_prompt: str,
    user_prompt: str,
    *,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    stream: bool = False,
) -> LLMRequest:
    return LLMRequest(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
        messages=[
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt),
        ],
    )
