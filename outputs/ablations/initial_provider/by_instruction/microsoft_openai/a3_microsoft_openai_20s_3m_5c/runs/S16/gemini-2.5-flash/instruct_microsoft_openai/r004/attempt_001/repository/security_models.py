from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime

@dataclass
class SecretMetadata:
    secret_id: str
    provider: str
    last_rotated: Optional[datetime] = None
    next_rotation_due: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)
    notes: Optional[str] = None
    status: Optional[str] = None # e.g., "active", "pending_rotation", "expired"

@dataclass
class SecretRotationSummary:
    secret_id: str
    provider: str
    rotation_status: str # e.g., "Successful", "Failed", "Pending"
    last_rotation_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    error_message: Optional[str] = None

@dataclass
class SecretAuditEntry:
    secret_id: str
    timestamp: datetime
    action: str # e.g., "access", "creation", "rotation", "deletion"
    actor: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
