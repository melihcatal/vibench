from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any, Generator


class ChatMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role: str
    content: str


class ModelRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    deployment: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None


class ModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    content: str
    usage: Optional[Dict[str, Any]] = None
