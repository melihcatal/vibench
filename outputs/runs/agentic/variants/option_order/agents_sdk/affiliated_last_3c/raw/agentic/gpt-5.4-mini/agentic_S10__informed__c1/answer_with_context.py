from __future__ import annotations

from model_client import complete_text
from model_models import ChatRequest


def answer_with_context(context: str, question: str) -> str:
    request = ChatRequest(
        model_family="reasoning",
        system="Answer the question using only the provided context when possible.",
        context=context,
        user=question,
        temperature=0.2,
        max_tokens=400,
    )
    return complete_text(request).text
