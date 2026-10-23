from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages
from model_models import ChatResult


_PROVIDER = "openai"
_DEFAULT_TTS_BRIEF_MODEL = "gpt-4o-mini"


def spoken_brief(text: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> ChatResult:
    """Generate a concise spoken brief from model output using OpenAI Chat Completions."""
    model_name = model or get_model_name("spoken_brief", _DEFAULT_TTS_BRIEF_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(
        system="Rewrite the input as a short spoken brief with natural pauses and plain language.",
        user=text,
    )
    response = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.4,
    )
    content = response.choices[0].message.content or ""
    return ChatResult(provider=_PROVIDER, model=model_name, content=content)
