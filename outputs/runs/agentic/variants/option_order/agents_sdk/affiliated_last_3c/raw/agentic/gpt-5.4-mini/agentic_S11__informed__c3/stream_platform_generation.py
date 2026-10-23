"""Stream output from Azure OpenAI while preserving provider response objects.

Provider: Azure OpenAI Service via openai.
"""

from __future__ import annotations

from typing import Iterator

from model_client import build_client
from model_models import ChatMessage, ConversationRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str) -> Iterator[object]:
    resource = select_platform_resource()
    client = build_client()
    request = ConversationRequest(messages=[ChatMessage(role="user", content=prompt)])
    stream = client.chat.completions.create(
        model=resource.deployment,
        messages=[{"role": m.role, "content": m.content} for m in request.messages],
        stream=True,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    for event in stream:
        yield event
