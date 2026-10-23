from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class PubSubMessage(BaseModel):
    data: Dict[str, Any]
    message_id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None


class MessageSummaryRequest(BaseModel):
    message_content: str


class MessageSafetyRequest(BaseModel):
    text_content: str


class MessageTranslationRequest(BaseModel):
    text_content: str
    target_language: str


class MessageAuditRecord(BaseModel):
    message_id: str
    timestamp: str
    original_payload: Dict[str, Any]
    processed_payload: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    safety_score: Optional[float] = None
    translated_content: Optional[str] = None
