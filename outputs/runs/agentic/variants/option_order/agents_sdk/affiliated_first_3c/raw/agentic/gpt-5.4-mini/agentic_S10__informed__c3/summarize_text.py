from __future__ import annotations

from model_client import chat_completion
from model_models import ChatMessage, LLMRequest


def summarize_text(long_text: str) -> str:
    request = LLMRequest(
        model_family="gpt-4o-mini",
        messages=[
            ChatMessage(role="system", content="You summarize long text into a concise, accurate summary."),
            ChatMessage(role="user", content=f"Summarize the following text:\n\n{long_text}"),
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return chat_completion(request).text
