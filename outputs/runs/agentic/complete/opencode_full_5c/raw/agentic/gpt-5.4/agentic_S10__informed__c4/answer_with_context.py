from __future__ import annotations

from model_client import choose_chat_model, complete_chat
from model_models import ChatRequest, Message


def answer_with_context(question: str, context: str) -> str:
    request = ChatRequest(
        system="Answer the question using only the provided context. If the answer is not in the context, say so clearly.",
        messages=[
            Message(
                role="user",
                content=f"Context:\n{context}\n\nQuestion: {question}",
            )
        ],
        model=choose_chat_model("qa"),
        temperature=0.1,
        max_output_tokens=400,
    )
    return complete_chat(request).text
