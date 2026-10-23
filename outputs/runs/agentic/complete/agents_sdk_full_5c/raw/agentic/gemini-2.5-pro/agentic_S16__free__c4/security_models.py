from pydantic import BaseModel, Field
from typing import Dict, Any

class SecretFetchError(Exception):
    """Custom exception for secret fetching failures."""
    pass

class ParsedJSONSecret(BaseModel):
    """
    A model to represent a parsed JSON secret, ensuring it has expected fields.
    """
    username: str
    password: str
    host: str
    port: int
    extra_config: Dict[str, Any] = Field(default_factory=dict)

class SecretRotationEvent(BaseModel):
    """
    Model for summarizing a secret rotation event.
    """
    secret_name: str
    status: str # e.g., 'SUCCESS', 'FAILURE'
    details: str
    source_system: str = "SecretManagementSystem"

