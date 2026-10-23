from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class SecretPayload:
    secret_id: str
    key_field: Optional[str] = None
    secret_value: Optional[str] = None
    content_type: Optional[str] = None
    tags: Optional[Dict[str, str]] = None

@dataclass
class SecretRotationResult:
    secret_id: str
    new_version_id: str
    status: str
    message: Optional[str] = None

@dataclass
class SecretSummary:
    secret_id: str
    created_on: str
    expires_on: Optional[str] = None
    enabled: bool
    tags: Optional[Dict[str, str]] = None
    latest_version_id: Optional[str] = None
    latest_version_enabled: Optional[bool] = None

@dataclass
class AuditNote:
    note_id: str
    secret_id: str
    content: str
    timestamp: str
    labels: Optional[Dict[str, str]] = None
