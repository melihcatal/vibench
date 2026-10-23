from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SecretInfo:
    name: str
    value: str
    properties: Optional[Dict[str, Any]] = None

@dataclass
class SecretRotationSummary:
    secret_id: str
    current_version: str
    last_rotated: Optional[str] = None
    next_rotation_due: Optional[str] = None
    rotation_status: Optional[str] = None

@dataclass
class AuditNote:
    id: str
    text: str
    labels: Dict[str, str]

@dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    target_language: str
