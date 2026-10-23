from typing import List, Dict, Any, Iterator, TypedDict


class ChatMessage(TypedDict):
    role: str
    content: str


class ChatResponse(TypedDict):
    content: str
    metadata: Dict[str, Any]
