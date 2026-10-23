from pydantic import BaseModel
from typing import Optional, Dict, Any


class Secret:
    def __init__(self, name: str, value: Any, version: Optional[str] = None):
        self.name = name
        self.value = value
        self.version = version


class SecretRotationStatus(BaseModel):
    secret_id: str
    status: str
    summary: Optional[str] = None


class UnsafeTextDetection(BaseModel):
    text: str
    is_unsafe: bool
    details: Optional[Dict[str, float]] = None


class AuditEmbedding(BaseModel):
    audit_note: str
    embedding: list[float]


class TranslatedRunbook(BaseModel):
    original_text: str
    translated_text: str
    target_language: str
