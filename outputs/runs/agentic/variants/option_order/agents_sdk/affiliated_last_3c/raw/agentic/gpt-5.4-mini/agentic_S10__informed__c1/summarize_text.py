from __future__ import annotations

from model_client import complete_text
from model_models import ChatRequest


def summarize_text(long_text: str) -> str:
    request = ChatRequest(
        model_family="summary",
        system="You are a concise summarization assistant.",
        user=f"Summarize the following text in a few bullet points:\n\n{long_text}",
        temperature=0.2,
        max_tokens=300,
    )
    return complete_text(request).text
