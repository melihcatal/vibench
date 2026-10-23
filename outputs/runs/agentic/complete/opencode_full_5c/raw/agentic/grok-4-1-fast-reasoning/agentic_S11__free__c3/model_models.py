from typing import TypedDict, List, Optional, Any


class ChatMessage(TypedDict):
    role: str
    content: str


class ChatRequest(TypedDict):
    messages: List[ChatMessage]
    temperature: Optional[float]
    max_tokens: Optional[int]


class Usage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class PlatformMetadata(TypedDict):
    request_id: str
    system_fingerprint: Optional[str]
    finish_reason: str
    usage: Usage
