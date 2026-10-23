from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SecretRequest(BaseModel):
    secret_id: str
    version_id: Optional[str] = "latest"
    project_id: Optional[str] = None


class SecretResponse(BaseModel):
    secret_value: str
    version_id: str
    secret_id: str
    created_at: Optional[str] = None
    labels: Optional[Dict[str, str]] = Field(default_factory=dict)
    notes: Optional[str] = None


class SecretVersionInfo(BaseModel):
    version_id: str
    state: str
    created_at: str
    destroy_at: Optional[str] = None


def normalize_secret_response(
    secret_id: str, version_id: str, secret_value: str, **kwargs
) -> SecretResponse:
    return SecretResponse(
        secret_id=secret_id, version_id=version_id, secret_value=secret_value, **kwargs
    )
