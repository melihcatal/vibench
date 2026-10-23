from typing import TypedDict, List, Dict, Any


class ChatMessage(TypedDict):
    role: str
    content: str


class ModelRequest(TypedDict):
    messages: List[ChatMessage]
    max_tokens: int
    temperature: float


class ModelResponse(TypedDict):
    content: str
    usage: Dict[str, int]
    model: str
