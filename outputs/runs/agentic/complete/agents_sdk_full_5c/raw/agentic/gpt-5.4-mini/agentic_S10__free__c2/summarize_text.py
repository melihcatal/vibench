from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages
from model_models import ChatResult


_PROVIDER = "openai"
_DEFAULT_SUMMARY_MODEL = "gpt-4o-mini"


def summarize_text(text: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> ChatResult:
    """Summarize long text using OpenAI Chat Completions."""
    model_name = model or get_model_name("summarize_text", _DEFAULT_SUMMARY_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(
        system="You are a concise expert summarizer.",
        user=f"Summarize the following text in a few bullet points:\n\n{text}",
    )
    response = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.2,
    )
    content = response.choices[0].message.content or ""
    return ChatResult(provider=_PROVIDER, model=model_name, content=content)
