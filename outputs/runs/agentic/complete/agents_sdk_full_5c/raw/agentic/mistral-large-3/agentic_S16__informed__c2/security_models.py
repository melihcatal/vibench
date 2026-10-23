from pydantic import BaseModel
from typing import Dict, Any, Optional

class SecretResponse(BaseModel):
    name: str
    value: str
    version: str
    enabled: bool = True

class JsonSecretResponse(BaseModel):
    name: str
    value: Dict[str, Any]
    version: str

class RotationSummary(BaseModel):
    secret_name: str
    current_version: str
    previous_version: Optional[str]
    rotation_status: str

class SafetyCheckResult(BaseModel):
    is_safe: bool
    violations: list[str]

class EmbeddingResponse(BaseModel):
    embedding: list[float]
    model: str

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str