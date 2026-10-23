from typing import Optional, Dict, Any
from pydantic import BaseModel

class SecretPayload(BaseModel):
    secret_id: str
    version: Optional[str] = "latest"
    project_id: str
    key_field: Optional[str] = None

class DbSecretPayload(SecretPayload):
    # No additional fields for now, but could be extended for specific DB types
    pass

class JsonSecretPayload(SecretPayload):
    # No additional fields for now
    pass

class RotateSecretPayload(BaseModel):
    secret_id: str
    project_id: str
    new_secret_data: str
    version_id: Optional[str] = None # For specific version to rotate or stage
    stage: Optional[str] = None # For staging a new version

class SecretRotationSummaryPayload(BaseModel):
    project_id: str
    filter: Optional[str] = None # e.g., "labels.env=production"

class SecretLabelSafetyPayload(BaseModel):
    project_id: str
    secret_id: str
    version: Optional[str] = "latest"

class SecretAuditEmbeddingPayload(BaseModel):
    project_id: str
    secret_id: str
    audit_note: str

class RunbookTranslatePayload(BaseModel):
    project_id: str
    text_to_translate: str
    target_language: str = "en"
    source_language: Optional[str] = None

class SecretOutput(BaseModel):
    secret_id: str
    value: Any

class SecretVersionOutput(BaseModel):
    secret_id: str
    version: str
    state: str
    create_time: str
    destroy_time: Optional[str] = None

class RotationSummaryOutput(BaseModel):
    secret_id: str
    current_version: Optional[str] = None
    last_rotation: Optional[str] = None
    rotation_period_days: Optional[int] = None

class LabelSafetyOutput(BaseModel):
    secret_id: str
    unsafe_labels: Dict[str, str]
    unsafe_notes: Dict[str, str]
    overall_safe: bool

class AuditEmbeddingOutput(BaseModel):
    secret_id: str
    embedding: list[float]

class TranslatedRunbookOutput(BaseModel):
    original_text: str
    translated_text: str
    target_language: str
    source_language: Optional[str] = None
