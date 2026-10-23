from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretResponse:
    """Normalized secret response model."""
    value: str
    metadata: Optional[Dict[str, Any]] = None
    version: Optional[str] = None


@dataclass
class SecretRotationRequest:
    """Request model for secret rotation."""
    secret_id: str
    new_value: str
    project_id: Optional[str] = None
    region: Optional[str] = None
    vault_url: Optional[str] = None


@dataclass
class SecretAuditNote:
    """Model for secret audit notes."""
    secret_id: str
    notes: str
    timestamp: str
    labels: Optional[Dict[str, str]] = None