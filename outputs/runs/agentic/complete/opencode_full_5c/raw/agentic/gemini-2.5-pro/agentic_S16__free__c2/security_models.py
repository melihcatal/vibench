from typing import Dict, Any
from pydantic import BaseModel, Field


class SecretPayload(BaseModel):
    """Represents a generic secret payload."""

    secret_id: str = Field(..., description="The ID of the secret.")
    project_id: str = Field(..., description="The Google Cloud project ID.")
    version: str = Field(default="latest", description="The secret version.")


class ParsedJSONSecret(BaseModel):
    """Represents a secret whose payload is a JSON object."""

    username: str
    password: str
    host: str
    port: int
    dbname: str


class SecretRotationEvent(BaseModel):
    """Represents a secret rotation event for summarization."""

    secret_id: str
    status: str
    notes: str
