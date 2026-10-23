from __future__ import annotations

from typing import Iterator

from model_client import stream_chat_completion
from model_models import ChatMessage, LLMRequest


def stream_completion(prompt: str) -> Iterator[str]:
    request = LLMRequest(
        model_family="gpt-4o-mini",
        messages=[ChatMessage(role="user", content=prompt)],
        temperature=0.3,
        max_tokens=500,
    )
    for chunk in stream_chat_completion(request):
        if chunk.text:
            yield chunk.text
