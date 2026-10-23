from typing import Dict, Any, Optional
from pydantic import BaseModel


class SecretResponse(BaseModel):
    """Normalized secret response model."""
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SecretRequest(BaseModel):
    """Normalized secret request model."""
    secret_id: str
    version_id: Optional[str] = None
    project_id: Optional[str] = None
    vault_url: Optional[str] = None