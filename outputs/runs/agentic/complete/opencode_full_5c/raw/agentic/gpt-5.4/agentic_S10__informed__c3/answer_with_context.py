from __future__ import annotations

from model_client import complete_text, default_config
from model_models import ChatTurn, LLMRequest


def answer_with_context(question: str, context: str) -> str:
    request = LLMRequest(
        system="Answer the question using only the supplied context. If the answer is not in context, say that directly.",
        messages=[
            ChatTurn(
                role="user",
                content=f"Context:\n{context}\n\nQuestion: {question}",
            )
        ],
        config=default_config("qa", max_output_tokens=300, temperature=0.1),
    )
    return complete_text(request).text.strip()
