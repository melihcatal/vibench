from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class ParsedSecret:
    """A simple model for a secret parsed from JSON."""
    name: str
    data: Dict[str, Any]

@dataclass
class SecretRotationInfo:
    """Model for summarizing secret rotation status."""
    secret_name: str
    last_rotated: str | None
    next_rotation: str | None
    status: str

@dataclass
class TextSafetyResult:
    """Model for text safety analysis results."""
    text: str
    is_safe: bool
    flags: List[str]

@dataclass
class AuditEmbedding:
    """Model for storing an audit note and its vector embedding."""
    note_id: str
    text: str
    embedding: List[float]

@dataclass
class TranslatedText:
    """Model for storing original and translated text."""
    original_text: str
    translated_text: str
    target_language: str
