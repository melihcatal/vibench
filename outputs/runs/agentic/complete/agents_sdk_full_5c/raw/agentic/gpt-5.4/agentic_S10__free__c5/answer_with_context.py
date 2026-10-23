from __future__ import annotations

from typing import Iterable

from model_client import create_chat_completion
from model_models import ChatMessage, GenerationRequest, join_context


def answer_with_context(question: str, context_parts: Iterable[str], model: str = "gpt-4o-mini") -> str:
    context = join_context(list(context_parts))
    request = GenerationRequest(
        model=model,
        temperature=0.1,
        max_tokens=300,
        messages=[
            ChatMessage(
                role="system",
                content="Answer questions only using the supplied context. If the answer is not in the context, say that explicitly.",
            ),
            ChatMessage(
                role="user",
                content=f"Context:\n{context}\n\nQuestion: {question}",
            ),
        ],
    )
    return create_chat_completion(request).text
