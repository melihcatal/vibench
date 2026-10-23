from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages
from model_models import ChatResult


_PROVIDER = "openai"
_DEFAULT_SAFETY_MODEL = "gpt-4o-mini"


def prompt_safety(text: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> ChatResult:
    """Check prompts and generated text for unsafe content using OpenAI."""
    model_name = model or get_model_name("prompt_safety", _DEFAULT_SAFETY_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(
        system="Classify whether the text contains unsafe content. Respond with a short verdict and rationale.",
        user=text,
    )
    response = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0,
    )
    content = response.choices[0].message.content or ""
    return ChatResult(provider=_PROVIDER, model=model_name, content=content)
