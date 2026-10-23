from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, run_chat
from model_models import ChatRequest


def answer_with_context(question: str, context: str) -> str:
    request = ChatRequest(
        system_prompt=(
            "You answer questions using only the provided context. "
            "If the answer is not contained in the context, say you do not know."
        ),
        user_prompt=(
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer with a short, direct response and cite the supporting detail in plain language."
        ),
        model=DEFAULT_CHAT_MODEL,
        temperature=0.1,
        max_tokens=220,
    )
    return run_chat(request).text
