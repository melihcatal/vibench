from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


class StructuredLog(BaseModel):
    message: str
    severity: str = "INFO"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None
    request_method: Optional[str] = None
    request_url: Optional[str] = None
    response_status: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None


class LogQueryResponse(BaseModel):
    entries: List[Dict[str, Any]]


class IncidentSummaryRequest(BaseModel):
    error_logs: List[str]


class IncidentSummaryResponse(BaseModel):
    summary: str


class ContentSafetyRequest(BaseModel):
    text: str


class ContentSafetyResponse(BaseModel):
    is_safe: bool
    reasons: List[str] = []


class TranslationRequest(BaseModel):
    text: str
    target_locale: str


class TranslationResponse(BaseModel):
    translated_text: str


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]
