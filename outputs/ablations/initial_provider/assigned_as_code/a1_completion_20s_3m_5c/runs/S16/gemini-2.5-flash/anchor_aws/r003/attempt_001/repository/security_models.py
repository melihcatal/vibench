from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class SecretPayload(BaseModel):
    secret_id: str = Field(..., description="The ID or ARN of the secret to retrieve.")
    key_field: Optional[str] = Field(None, description="Optional key to extract from a JSON secret string.")
    version_id: Optional[str] = Field(None, description="Specific version of the secret to retrieve.")
    version_stage: Optional[str] = Field(None, description="Specific stage of the secret to retrieve (e.g., AWSCURRENT).")


class SecretResponse(BaseModel):
    name: str
    arn: str
    value: Any
    created_date: Optional[str] = None
    version_id: Optional[str] = None
    version_stages: Optional[list] = None


class RotationSummary(BaseModel):
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    rotation_status: Optional[str] = None


class SecretLabelSafetyRequest(BaseModel):
    secret_id: str
    labels: Dict[str, str] = Field(default_factory=dict, description="Labels associated with the secret.")
    notes: Optional[str] = Field(None, description="Notes associated with the secret.")


class SecretLabelSafetyResponse(BaseModel):
    secret_id: str
    unsafe_labels_found: bool
    unsafe_notes_found: bool
    details: Dict[str, Any] = Field(default_factory=dict)


class SecretAuditEmbeddingRequest(BaseModel):
    secret_id: str
    audit_notes: str = Field(..., description="Audit notes to embed for semantic search.")


class SecretAuditEmbeddingResponse(BaseModel):
    secret_id: str
    embedding: list[float]


class RunbookTranslateRequest(BaseModel):
    secret_id: str
    runbook_notes: str = Field(..., description="Runbook notes to translate.")
    target_language: str = Field(..., description="Target language for translation (e.g., 'es', 'fr', 'de').")


class RunbookTranslateResponse(BaseModel):
    secret_id: str
    translated_notes: str
    source_language: Optional[str] = None
    target_language: str
