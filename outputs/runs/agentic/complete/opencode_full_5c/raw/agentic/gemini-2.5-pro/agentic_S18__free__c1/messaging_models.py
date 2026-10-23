from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class MessagePayload(BaseModel):
    message_id: str
    text: str
    sender: str
    timestamp: str


class ProcessedMessage(BaseModel):
    original_payload: MessagePayload
    is_safe: Optional[bool] = None
    safety_scores: Optional[Dict[str, float]] = None
    translated_text: Optional[str] = None
    summary: Optional[str] = None
    audit_id: Optional[str] = None


class BatchMessage(BaseModel):
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = Field(default_factory=dict)
