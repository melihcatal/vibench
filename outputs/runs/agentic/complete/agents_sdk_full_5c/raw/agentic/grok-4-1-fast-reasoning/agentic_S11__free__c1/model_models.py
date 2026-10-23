from typing import TypedDict, List, Any, Optional

class ChatMessage(TypedDict):
    role: str
    content: str

class ChatRequest(TypedDict):
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int]
    stream: Optional[bool]

class Usage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
