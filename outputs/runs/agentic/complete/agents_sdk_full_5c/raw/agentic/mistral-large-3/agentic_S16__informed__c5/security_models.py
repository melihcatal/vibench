from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretResponse:
    """Standardized response model for secret retrieval."""
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SecretRequest:
    """Standardized request model for secret operations."""
    secret_id: str
    version_id: Optional[str] = None
    project_id: Optional[str] = None
    region_name: Optional[str] = None
    vault_url: Optional[str] = None