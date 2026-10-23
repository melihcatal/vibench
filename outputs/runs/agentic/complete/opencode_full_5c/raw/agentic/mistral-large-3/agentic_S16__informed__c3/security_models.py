from typing import Dict, Any, Optional
from pydantic import BaseModel


class SecretRequest(BaseModel):
    secret_name: str
    version_stage: Optional[str] = "AWSCURRENT"
    version_id: Optional[str] = None


class SecretResponse(BaseModel):
    secret_value: str
    metadata: Dict[str, Any]


class RotationSummary(BaseModel):
    secret_name: str
    current_version: str
    previous_version: Optional[str]
    rotation_enabled: bool
    last_rotation_date: Optional[str]
    next_rotation_date: Optional[str]


class SecretLabelCheck(BaseModel):
    secret_name: str
    labels: Dict[str, str]
    is_safe: bool
    unsafe_reasons: Optional[list[str]]


class EmbeddingRequest(BaseModel):
    text: str
    model_id: Optional[str] = "amazon.titan-embed-text-v1"


class EmbeddingResponse(BaseModel):
    embedding: list[float]
    model_id: str


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None


class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: Optional[str]
