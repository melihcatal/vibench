from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages
from model_models import ChatResult


_PROVIDER = "openai"
_DEFAULT_QA_MODEL = "gpt-4o"


def answer_with_context(question: str, context: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> ChatResult:
    """Answer a question using provided context with OpenAI Chat Completions."""
    model_name = model or get_model_name("answer_with_context", _DEFAULT_QA_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(
        system="Answer using only the provided context. If the answer is not in the context, say you cannot determine it.",
        user=f"Context:\n{context}\n\nQuestion:\n{question}",
    )
    response = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.1,
    )
    content = response.choices[0].message.content or ""
    return ChatResult(provider=_PROVIDER, model=model_name, content=content)
