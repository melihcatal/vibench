from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SecretResponse(BaseModel):
    """Normalized response model for secret retrieval."""
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SecretRotationRequest(BaseModel):
    """Request model for secret rotation."""
    secret_id: str
    project_id: Optional[str] = None
    version_id: Optional[str] = None
    rotation_strategy: str = "latest"


class SecretLabelCheckRequest(BaseModel):
    """Request model for secret label safety checks."""
    labels: Dict[str, str]
    notes: Optional[str] = None