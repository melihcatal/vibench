# [HELPER] security_models.py
from pydantic import BaseModel, Field

class SecretReference(BaseModel):
    name: str = Field(description="Identifier used by the secret manager")
    provider: str = Field(description="Secret manager provider, e.g. gcp, azure, aws")

class SecretValue(BaseModel):
    value: str = Field(description="Plain secret payload")
    version_id: str = Field(default=None, description="Version identifier when applicable")

class JSONSecret(BaseModel):
    data: dict = Field(description="Parsed JSON payload")
    version_id: str = Field(default=None)

class RotationStatus(BaseModel):
    secret_name: str
    current_version: str
    next_rotation_due: str  # ISO8601 timestamp
    is_stage_complete: bool

class LabelSafetyCheck(BaseModel):
    unsafe_labels: list[str] = []
    notes: str = ''
    safe: bool = True

class EmbeddingContext(BaseModel):
    secret_name: str
    notes: str
    embedding: list[float]
