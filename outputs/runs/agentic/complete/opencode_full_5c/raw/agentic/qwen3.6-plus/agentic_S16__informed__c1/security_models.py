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
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    tags: dict = field(default_factory=dict)
    description: Optional[str] = None


@dataclass
class RotationSummaryRequest:
    secret_id: str
    include_history: bool = True


@dataclass
class RotationSummaryResponse:
    secret_id: str
    rotation_status: str
    last_rotation_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    rotation_interval_days: Optional[int] = None
    rotation_history: list = field(default_factory=list)
    summary_text: str = ""


@dataclass
class LabelSafetyRequest:
    label_text: str
    secret_id: str


@dataclass
class LabelSafetyResponse:
    label_text: str
    is_safe: bool
    flagged_categories: list = field(default_factory=list)
    confidence_scores: dict = field(default_factory=dict)
    details: str = ""


@dataclass
class AuditEmbeddingRequest:
    audit_notes: str
    secret_id: str


@dataclass
class AuditEmbeddingResponse:
    secret_id: str
    audit_notes: str
    embedding: list = field(default_factory=list)
    model_used: str = ""
    dimension: int = 0


@dataclass
class TranslationRequest:
    source_text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslationResponse:
    source_text: str
    translated_text: str
    source_language: str = ""
    target_language: str = ""
    model_used: str = ""


def normalize_secret_response(raw_response: dict) -> SecretResponse:
    return SecretResponse(
        secret_id=raw_response.get("Name", ""),
        secret_value=raw_response.get("SecretString", raw_response.get("SecretBinary")),
        version_id=raw_response.get("VersionId"),
        version_stages=raw_response.get("VersionIdsToStages", {}).get(
            raw_response.get("VersionId", ""), []
        ),
        created_date=raw_response.get("CreatedDate"),
        rotation_enabled=raw_response.get("RotationEnabled", False),
        rotation_lambda_arn=raw_response.get("RotationLambdaARN"),
        last_rotated_date=raw_response.get("LastRotatedDate"),
        next_rotation_date=raw_response.get("NextRotationDate"),
        tags={t.get("Key"): t.get("Value") for t in raw_response.get("Tags", [])},
        description=raw_response.get("Description"),
    )


def build_secret_request(
    secret_id: str, version_stage: Optional[str] = None
) -> SecretRequest:
    return SecretRequest(
        secret_id=secret_id.strip(),
        version_stage=version_stage or "AWSCURRENT",
    )
