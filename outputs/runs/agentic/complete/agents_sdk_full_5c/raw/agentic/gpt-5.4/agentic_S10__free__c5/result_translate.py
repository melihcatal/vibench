from __future__ import annotations

from model_client import create_chat_completion
from model_models import ChatMessage, GenerationRequest, coerce_text


def translate_result(text: str, target_language: str, model: str = "gpt-4o-mini") -> str:
    source_text = coerce_text(text)
    request = GenerationRequest(
        model=model,
        temperature=0.2,
        max_tokens=500,
        messages=[
            ChatMessage(
                role="system",
                content="You are a professional translator. Preserve meaning, tone, formatting, and named entities.",
            ),
            ChatMessage(
                role="user",
                content=f"Translate the following text into {target_language}:\n\n{source_text}",
            ),
        ],
    )
    return create_chat_completion(request).text
