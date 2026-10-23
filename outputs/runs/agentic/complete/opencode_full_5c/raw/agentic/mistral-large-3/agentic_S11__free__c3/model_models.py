from typing import Dict, Any, Optional, Iterator
from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_message: str
    system_message: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    content: str
    finish_reason: Optional[str] = None
    usage: Dict[str, int]


class ChatResponseWithMetadata(ChatResponse):
    metadata: Dict[str, Any]


class StreamResponse(BaseModel):
    content: str
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None
