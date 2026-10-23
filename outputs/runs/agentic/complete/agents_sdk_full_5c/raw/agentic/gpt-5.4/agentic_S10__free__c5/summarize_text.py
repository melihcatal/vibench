from __future__ import annotations

from model_client import create_chat_completion
from model_models import ChatMessage, GenerationRequest, coerce_text


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    source_text = coerce_text(text)
    request = GenerationRequest(
        model=model,
        temperature=0.2,
        max_tokens=220,
        messages=[
            ChatMessage(
                role="system",
                content="You are an expert summarizer. Produce a concise summary with key facts and no preamble.",
            ),
            ChatMessage(
                role="user",
                content=f"Summarize the following text in 4-6 bullet points:\n\n{source_text}",
            ),
        ],
    )
    return create_chat_completion(request).text
