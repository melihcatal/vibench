from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[str] = None
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


class BatchMessage(BaseModel):
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


class PublishResponse(BaseModel):
    message_ids: List[str]


class ConsumeResponse(BaseModel):
    message: Optional[Message] = None
