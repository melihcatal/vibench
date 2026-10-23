from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class SecretMetadata:
    secret_id: str
    creation_date: str
    last_accessed_date: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None

@dataclass
class SecretRotationStatus:
    secret_id: str
    is_compliant: bool
    compliance_details: Optional[Dict[str, Any]] = None
    last_rotation_date: Optional[str] = None
    next_rotation_due: Optional[str] = None

@dataclass
class AuditNote:
    note_id: str
    timestamp: str
    actor: str
    action: str
    details: Optional[str] = None
    embedding: Optional[List[float]] = None

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
