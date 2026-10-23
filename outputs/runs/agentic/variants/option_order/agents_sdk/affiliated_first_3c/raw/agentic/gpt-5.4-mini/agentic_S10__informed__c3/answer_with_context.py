from __future__ import annotations

from model_client import chat_completion
from model_models import ChatMessage, LLMRequest


def answer_with_context(question: str, context: str) -> str:
    request = LLMRequest(
        model_family="gpt-4o-mini",
        messages=[
            ChatMessage(role="system", content="Answer the question using only the provided context when possible."),
            ChatMessage(role="user", content=f"Context:\n{context}\n\nQuestion:\n{question}"),
        ],
        temperature=0.2,
        max_tokens=400,
    )
    return chat_completion(request).text
