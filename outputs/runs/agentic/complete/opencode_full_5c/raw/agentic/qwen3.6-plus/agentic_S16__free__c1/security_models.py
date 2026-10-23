import os
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum


class SecretType(Enum):
    API_KEY = "api_key"
    DATABASE = "database"
    JSON_CONFIG = "json_config"
    CERTIFICATE = "certificate"
    GENERIC = "generic"


class RotationStatus(Enum):
    NOT_ENABLED = "not_enabled"
    IN_PROGRESS = "in_progress"
    SCHEDULED = "scheduled"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass
class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    region: Optional[str] = None
    secret_type: SecretType = SecretType.GENERIC

    def to_dict(self) -> dict:
        return {
            "secret_name": self.secret_name,
            "version_id": self.version_id,
            "version_stage": self.version_stage,
            "region": self.region,
            "secret_type": self.secret_type.value,
        }


@dataclass
class SecretResponse:
    secret_name: str
    secret_value: Optional[str] = None
    version_id: Optional[str] = None
    version_stages: list = field(default_factory=list)
    created_date: Optional[str] = None
    rotation_enabled: bool = False
    rotation_status: Optional[str] = None
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    labels: list = field(default_factory=list)
    description: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def parsed_json(self) -> dict:
        if self.secret_value is None:
            return {}
        try:
            return json.loads(self.secret_value)
        except (json.JSONDecodeError, TypeError):
            return {}


@dataclass
class RotationSummary:
    secret_name: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: dict = field(default_factory=dict)
    last_rotation_status: Optional[str] = None
    last_rotation_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    version_stages_summary: dict = field(default_factory=dict)
    summary_text: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SafetyCheckResult:
    secret_name: str
    label: str
    is_safe: bool
    flagged_terms: list = field(default_factory=list)
    confidence: float = 0.0
    explanation: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EmbeddingResult:
    secret_name: str
    audit_note: str
    embedding: list = field(default_factory=list)
    model: str = ""
    dimensions: int = 0

    def to_dict(self) -> dict:
        return {
            "secret_name": self.secret_name,
            "audit_note": self.audit_note,
            "model": self.model,
            "dimensions": self.dimensions,
            "embedding_preview": self.embedding[:8] if self.embedding else [],
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str = ""
    source_language: str = "auto"
    target_language: str = "en"
    model: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_secret_name(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def build_secret_arn(region: str, account_id: str, secret_name: str) -> str:
    return f"arn:aws:secretsmanager:{region}:{account_id}:secret:{secret_name}"


def parse_aws_error(error_code: str, error_message: str) -> dict:
    return {
        "provider": "aws_secrets_manager",
        "error_code": error_code,
        "error_message": error_message,
        "retryable": error_code in ["ThrottlingException", "InternalServiceError"],
    }
