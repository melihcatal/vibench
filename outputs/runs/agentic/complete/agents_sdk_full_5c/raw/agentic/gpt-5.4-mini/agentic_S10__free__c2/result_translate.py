from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages
from model_models import ChatResult


_PROVIDER = "openai"
_DEFAULT_TRANSLATE_MODEL = "gpt-4o-mini"


def result_translate(text: str, target_language: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> ChatResult:
    """Translate generated model output using OpenAI Chat Completions."""
    model_name = model or get_model_name("result_translate", _DEFAULT_TRANSLATE_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(
        system="You are a precise translation engine.",
        user=f"Translate the following text into {target_language}:\n\n{text}",
    )
    response = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.2,
    )
    content = response.choices[0].message.content or ""
    return ChatResult(provider=_PROVIDER, model=model_name, content=content)
