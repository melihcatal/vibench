import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

from model_models import LLMRequest, LLMResult, normalize_text

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_BASE_URL = os.getenv("OPENAI_BASE_URL")


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=DEFAULT_BASE_URL)


def build_messages(system: Optional[str], user: str, context: Optional[str] = None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    content = user if context is None else f"Context:\n{context}\n\nQuestion/Task:\n{user}"
    messages.append({"role": "user", "content": content})
    return messages


def complete_chat(request: LLMRequest) -> LLMResult:
    client = get_client()
    model = request.model or DEFAULT_MODEL
    resp = client.chat.completions.create(
        model=model,
        messages=build_messages(request.system, request.prompt, request.context),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    text = resp.choices[0].message.content or ""
    return LLMResult(text=normalize_text(text), model=model, provider="openai")


def stream_chat(request: LLMRequest):
    client = get_client()
    model = request.model or DEFAULT_MODEL
    stream = client.chat.completions.create(
        model=model,
        messages=build_messages(request.system, request.prompt, request.context),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        if delta:
            yield delta
