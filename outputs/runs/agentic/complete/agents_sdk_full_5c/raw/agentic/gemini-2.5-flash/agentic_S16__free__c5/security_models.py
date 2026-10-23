from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class SecretMetadata:
    """
    Defines common metadata fields for a secret.
    """
    name: str
    provider: str
    description: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    created_time: Optional[str] = None
    last_rotated_time: Optional[str] = None
    next_rotation_time: Optional[str] = None

@dataclass
class SecretVersion:
    """
    Defines a specific version of a secret.
    """
    version_id: str
    payload: Any # The actual secret value (can be string, bytes, JSON object)
    created_time: Optional[str] = None
    enabled: bool = True

@dataclass
class SecretRotationStatus:
    """
    Summarizes the status of a secret's rotation.
    """
    secret_name: str
    last_rotation_success: bool
    last_rotation_time: Optional[str] = None
    next_rotation_due: Optional[str] = None
    days_until_due: Optional[int] = None
    health_status: str # e.g., "OK", "WARNING", "CRITICAL"

@dataclass
class AuditNote:
    """
    Represents an audit note associated with a secret.
    """
    note_id: str
    secret_name: str
    timestamp: str
    actor: str
    action: str
    details: str
    tags: List[str] = field(default_factory=list)

@dataclass
class TranslatedText:
    """
    Represents text translated into another language.
    """
    original_text: str
    translated_text: str
    source_language_code: str
    target_language_code: str
