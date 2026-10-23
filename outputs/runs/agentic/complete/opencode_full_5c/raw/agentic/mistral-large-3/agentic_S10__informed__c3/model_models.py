from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ModelRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: Optional[bool] = False
    response_format: Optional[Dict[str, Any]] = None


class ModelResponseChoice(BaseModel):
    message: ChatMessage
    delta: Optional[ChatMessage] = None
    finish_reason: Optional[str] = None


class ModelResponse(BaseModel):
    choices: List[ModelResponseChoice]
    id: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
