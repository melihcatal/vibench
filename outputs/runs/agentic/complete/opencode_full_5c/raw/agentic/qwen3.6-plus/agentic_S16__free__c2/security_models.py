from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    with_decryption: bool = True


@dataclass
class SecretResponse:
    secret_id: str
    secret_value: Any
    version_id: Optional[str] = None
    version_stages: list = field(default_factory=list)
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[dict] = None
    tags: list = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class RotationStatus:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[dict] = None
    current_version: Optional[str] = None
    pending_version: Optional[str] = None


@dataclass
class SecretLabelCheck:
    label_name: str
    is_safe: bool
    flagged_terms: list = field(default_factory=list)
    confidence: float = 0.0
    raw_analysis: Optional[str] = None


@dataclass
class AuditEmbedding:
    secret_id: str
    audit_text: str
    embedding: list = field(default_factory=list)
    model_used: str = ""
    dimension: int = 0


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str = "auto"
    target_language: str = "en"
    model_used: str = ""


def normalize_secret_value(raw_value: Any, parse_json: bool = False) -> Any:
    import json

    if isinstance(raw_value, bytes):
        raw_value = raw_value.decode("utf-8")
    if parse_json and isinstance(raw_value, str):
        try:
            return json.loads(raw_value)
        except (json.JSONDecodeError, TypeError):
            return raw_value
    return raw_value


def format_secret_tags(tags: list) -> dict:
    return {t.get("Key", ""): t.get("Value", "") for t in tags if isinstance(t, dict)}


def build_secret_request(
    secret_id: str, version_id: str = None, version_stage: str = None
) -> SecretRequest:
    return SecretRequest(
        secret_id=secret_id,
        version_id=version_id,
        version_stage=version_stage,
        with_decryption=True,
    )
