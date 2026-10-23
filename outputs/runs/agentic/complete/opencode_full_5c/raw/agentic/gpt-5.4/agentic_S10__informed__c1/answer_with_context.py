from __future__ import annotations

from typing import Iterable

from model_client import create_chat_completion
from model_models import ChatRequest, join_context_parts


def answer_with_context(
    question: str, context_parts: Iterable[str], model: str | None = None
) -> str:
    context = join_context_parts(context_parts)
    request = ChatRequest(
        system_prompt="You are an OpenAI question answering assistant. Answer only from the supplied context and say when the context is insufficient.",
        user_prompt=f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer using only the context.",
        model=model,
        temperature=0.1,
        max_tokens=300,
    )
    return create_chat_completion(request).text.strip()
