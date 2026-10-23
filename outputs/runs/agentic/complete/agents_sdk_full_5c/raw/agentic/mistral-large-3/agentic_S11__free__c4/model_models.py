from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class Message(BaseModel):
    role: str
    content: str

class ModelRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None

    def dict(self, **kwargs):
        payload = super().dict(**kwargs)
        payload["messages"] = [msg.dict() for msg in payload["messages"]]
        return payload