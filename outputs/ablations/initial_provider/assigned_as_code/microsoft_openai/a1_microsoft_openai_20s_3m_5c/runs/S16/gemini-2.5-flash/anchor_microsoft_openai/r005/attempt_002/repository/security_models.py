from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class SecretPayload:
    secret_id: str
    key_field: Optional[str] = None

@dataclass
class SecretResponse:
    value: Any

@dataclass
class SecretProperties:
    id: str
    name: str
    enabled: Optional[bool] = None
    expires_on: Optional[float] = None
    created_on: Optional[float] = None
    updated_on: Optional[float] = None
    tags: Optional[Dict[str, str]] = None
    content_type: Optional[str] = None
    recoverable_days: Optional[int] = None

@dataclass
class TranslationRequest:
    text: str
    to_language: str

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: list[float]

@dataclass
class ContentSafetyRequest:
    text: str

@dataclass
class ContentSafetyResponse:
    is_safe: bool
    moderation_result: Dict[str, Any]
