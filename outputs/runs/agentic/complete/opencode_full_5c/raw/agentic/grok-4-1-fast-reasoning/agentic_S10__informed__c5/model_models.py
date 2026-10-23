from typing import TypedDict, List, Dict, Any, Optional


class ChatMessage(TypedDict):
    role: str
    content: str


class LLMRequest(TypedDict):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float]
    max_tokens: Optional[int]


class LLMResponse(TypedDict):
    content: str
    model_used: str
