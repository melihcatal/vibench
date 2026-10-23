import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class SecretMetadata:
    name: str
    arn: str
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None


@dataclasses.dataclass
class RotationStatus:
    secret_name: str
    rotation_enabled: bool
    last_rotated_date: Optional[str] = None


@dataclasses.dataclass
class AuditNote:
    note_id: str
    content: str


@dataclasses.dataclass
class TranslatedText:
    source_text: str
    translated_text: str
    source_language_code: str
    target_language_code: str
