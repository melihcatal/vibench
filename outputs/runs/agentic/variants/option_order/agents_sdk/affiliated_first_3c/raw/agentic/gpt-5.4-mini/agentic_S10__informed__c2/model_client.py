from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, Iterator, List, Optional

from openai import OpenAI

from model_models import LLMRequest, LLMResponse, coerce_text

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_messages(system: str, user: str, context: Optional[str] = None) -> List[Dict[str, str]]:
    messages = [{"role": "system", "content": system}]
    if context:
        messages.append({"role": "user", "content": f"Context:\n{context}"})
    messages.append({"role": "user", "content": user})
    return messages


def chat_completion(request: LLMRequest) -> LLMResponse:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=request.model,
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
    )
    text = coerce_text(response.choices[0].message.content if response.choices else "")
    return LLMResponse(text=text, model=request.model, raw=response)


def stream_chat_completion(request: LLMRequest) -> Iterator[str]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=request.model,
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stream=True,
    )
    for chunk in stream:
        delta = getattr(chunk.choices[0].delta, "content", None) if chunk.choices else None
        if delta:
            yield delta


def parse_json_content(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def openai_embedding(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    client = get_openai_client()
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)
