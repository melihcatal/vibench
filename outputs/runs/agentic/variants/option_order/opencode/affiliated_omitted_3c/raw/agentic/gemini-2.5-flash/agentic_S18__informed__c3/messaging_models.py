import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class EventMessage(BaseModel):
    id: str
    type: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = Field(default_factory=dict)


class BatchEventMessage(BaseModel):
    id: str
    message_body: str
    message_attributes: Dict[str, str] = Field(default_factory=dict)


class MessageConsumptionResult(BaseModel):
    message_id: str
    receipt_handle: str
    body: Dict[str, Any]
    attributes: Dict[str, str]


class TranslationRequest(BaseModel):
    text: str
    source_language_code: str
    target_language_code: str


class TranslationResult(BaseModel):
    translated_text: str
    source_language_code: str
    target_language_code: str


class ContentSafetyRequest(BaseModel):
    text: str


class ContentSafetyResult(BaseModel):
    is_unsafe: bool
    moderation_labels: List[Dict[str, Any]]


class MessageSummaryRequest(BaseModel):
    message_content: str


class MessageSummaryResult(BaseModel):
    summary: str


class AuditRecord(BaseModel):
    message_id: str
    timestamp: str
    status: str
    payload: Dict[str, Any]
    processing_details: Optional[Dict[str, Any]] = None
