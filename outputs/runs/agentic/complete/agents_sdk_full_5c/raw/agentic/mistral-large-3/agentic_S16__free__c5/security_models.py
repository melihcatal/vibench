from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SecretRequest(BaseModel):
    """Standardized request model for secret retrieval."""
    secret_id: str = Field(..., description="The identifier of the secret.")
    version_id: Optional[str] = Field(
        "latest", description="The version of the secret to retrieve."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional metadata for the secret."
    )


class SecretResponse(BaseModel):
    """Standardized response model for secret retrieval."""
    value: str = Field(..., description="The retrieved secret value.")
    version: str = Field(..., description="The version of the retrieved secret.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the secret."
    )


class JSONSecretResponse(SecretResponse):
    """Standardized response model for JSON-formatted secrets."""
    value: Dict[str, Any] = Field(..., description="The parsed JSON secret value.")