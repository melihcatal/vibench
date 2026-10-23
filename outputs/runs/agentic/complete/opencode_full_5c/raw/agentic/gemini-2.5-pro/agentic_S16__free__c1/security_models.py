from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SecretValue:
    secret_id: str
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    version_id: Optional[str] = None
    version_stages: Optional[list] = None


@dataclass
class SecretRotationStatus:
    secret_id: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str] = None
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None


@dataclass
class UnsafeTextAnalysis:
    is_unsafe: bool
    reasons: Dict[str, float]


@dataclass
class AuditEmbedding:
    audit_text: str
    embedding: list[float]


@dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    target_language: str
