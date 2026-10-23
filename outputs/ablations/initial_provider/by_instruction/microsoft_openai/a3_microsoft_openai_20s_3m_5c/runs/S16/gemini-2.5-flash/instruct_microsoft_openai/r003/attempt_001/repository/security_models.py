import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class SecretItem:
    name: str
    value: Optional[str] = None
    arn: Optional[str] = None
    version_id: Optional[str] = None
    created_date: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SecretRotationSummary:
    secret_name: str
    last_rotated: Optional[str] = None
    next_rotation_due: Optional[str] = None
    status: Optional[str] = None
    issues: Optional[str] = None

@dataclass
class AuditNote:
    id: str
    secret_name: str
    timestamp: str
    note_content: str
    user: str
    action: str
    embedding: Optional[list[float]] = None

@dataclass
class TranslatedText:
    source_language: str
    target_language: str
    original_text: str
    translated_text: str
