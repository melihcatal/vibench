import os
from typing import List, Dict, Any, TypedDict


class ChatMessage(TypedDict):
    role: str
    content: str


class ChatRequest(TypedDict):
    model: str
    messages: List[ChatMessage]
    temperature: float
    max_tokens: int | None
    stream: bool


class Usage(TypedDict):
    prompt_tokens: int
    completion_tokens: int | None
    total_tokens: int | None


class PlatformMetadata(TypedDict):
    content: str
    model: str
    request_id: str
    usage: Usage | None


def normalize_chat_request(
    prompt: str, model: str, stream: bool = False
) -> ChatRequest:
    return ChatRequest(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)],
        temperature=0.7,
        max_tokens=1024,
        stream=stream,
    )
