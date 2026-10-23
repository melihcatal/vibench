from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    region: Optional[str] = None


@dataclass
class SecretResponse:
    secret_name: str
    secret_value: str
    version_id: str
    version_stages: list[str] = field(default_factory=list)
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    tags: dict[str, str] = field(default_factory=dict)
    description: Optional[str] = None


@dataclass
class RotationStatus:
    secret_name: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str]
    last_rotated_date: Optional[datetime]
    next_rotation_date: Optional[datetime]
    rotation_rules: dict[str, Any] = field(default_factory=dict)
    current_version_id: Optional[str] = None
    pending_version_id: Optional[str] = None


@dataclass
class AuditNote:
    secret_name: str
    note_text: str
    timestamp: datetime
    operator: Optional[str] = None
    action: Optional[str] = None


@dataclass
class EmbeddingResult:
    text: str
    embedding: list[float]
    model: str
    secret_name: Optional[str] = None


@dataclass
class SafetyCheckResult:
    text: str
    is_safe: bool
    categories: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    model: Optional[str] = None


@dataclass
class RotationSummary:
    secret_name: str
    summary_text: str
    rotation_health: str
    recommendations: list[str] = field(default_factory=list)


def normalize_secret_response(raw_response: dict) -> SecretResponse:
    secret_string = raw_response.get("SecretString", "")
    version_id = raw_response.get("VersionId", "")
    version_stages = raw_response.get("VersionStages", [])
    return SecretResponse(
        secret_name=raw_response.get("Name", ""),
        secret_value=secret_string,
        version_id=version_id,
        version_stages=version_stages,
        created_date=raw_response.get("CreatedDate"),
        tags={t["Key"]: t["Value"] for t in raw_response.get("Tags", [])},
        description=raw_response.get("Description"),
    )


def normalize_rotation_status(raw_response: dict) -> RotationStatus:
    return RotationStatus(
        secret_name=raw_response.get("Name", ""),
        rotation_enabled=raw_response.get("RotationEnabled", False),
        rotation_lambda_arn=raw_response.get("RotationLambdaARN"),
        last_rotated_date=raw_response.get("LastRotatedDate"),
        next_rotation_date=raw_response.get("NextRotationDate"),
        rotation_rules=raw_response.get("RotationRules", {}),
        current_version_id=raw_response.get("CurrentVersionId"),
        pending_version_id=raw_response.get("PendingVersionId"),
    )
