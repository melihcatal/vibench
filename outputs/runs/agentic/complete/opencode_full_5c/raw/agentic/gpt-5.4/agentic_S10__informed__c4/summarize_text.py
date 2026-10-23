from __future__ import annotations

from model_client import choose_chat_model, complete_chat
from model_models import ChatRequest, Message


def summarize_text(text: str, max_sentences: int = 5) -> str:
    request = ChatRequest(
        system="You are a precise summarization assistant.",
        messages=[
            Message(
                role="user",
                content=f"Summarize the following text in at most {max_sentences} sentences, focusing on key facts and outcomes.\n\n{text}",
            )
        ],
        model=choose_chat_model("summarize"),
        temperature=0.2,
        max_output_tokens=500,
    )
    return complete_chat(request).text
