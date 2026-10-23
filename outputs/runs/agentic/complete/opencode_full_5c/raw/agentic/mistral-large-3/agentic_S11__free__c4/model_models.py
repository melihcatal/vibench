from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000


class ChatResponse(BaseModel):
    content: str
    usage: Dict[str, int]
    model: str


class StreamResponseChunk(BaseModel):
    content: str
    chunk_metadata: Dict[str, Any]
