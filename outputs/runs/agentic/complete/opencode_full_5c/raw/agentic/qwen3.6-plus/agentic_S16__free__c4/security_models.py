import os
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    region: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class SecretResponse:
    secret_id: str
    secret_value: Any
    version_id: str
    version_stage: str
    created_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_aws_response(cls, secret_id: str, aws_response: dict) -> "SecretResponse":
        return cls(
            secret_id=secret_id,
            secret_value=aws_response.get("SecretString")
            or aws_response.get("SecretBinary"),
            version_id=aws_response.get("VersionId", ""),
            version_stage=aws_response.get("VersionStages", [""])[0]
            if aws_response.get("VersionStages")
            else "",
            created_at=aws_response.get("CreatedDate", "").isoformat()
            if isinstance(aws_response.get("CreatedDate"), datetime)
            else str(aws_response.get("CreatedDate", "")),
            metadata={
                "arn": aws_response.get("ARN", ""),
                "name": aws_response.get("Name", ""),
            },
        )


@dataclass
class RotationStatus:
    secret_id: str
    rotation_enabled: bool
    rotation_lambda_arn: str
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    rotation_rules: dict = field(default_factory=dict)
    current_version: Optional[str] = None
    pending_version: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_aws_describe(cls, secret_id: str, aws_response: dict) -> "RotationStatus":
        rotation_rules = aws_response.get("RotationRules", {})
        return cls(
            secret_id=secret_id,
            rotation_enabled=aws_response.get("RotationEnabled", False),
            rotation_lambda_arn=aws_response.get("RotationLambdaARN", ""),
            last_rotated_date=str(aws_response.get("LastRotatedDate", ""))
            if aws_response.get("LastRotatedDate")
            else None,
            next_rotation_date=str(aws_response.get("NextRotationDate", ""))
            if aws_response.get("NextRotationDate")
            else None,
            rotation_rules={
                "automatically_after_days": rotation_rules.get(
                    "AutomaticallyAfterDays"
                ),
                "duration": rotation_rules.get("Duration"),
                "schedule_expression": rotation_rules.get("ScheduleExpression"),
            },
            current_version=aws_response.get("VersionIdsToStages", {}).get(
                "AWSCURRENT", [None]
            )[0]
            if aws_response.get("VersionIdsToStages")
            else None,
            pending_version=aws_response.get("VersionIdsToStages", {}).get(
                "AWSPENDING", [None]
            )[0]
            if aws_response.get("VersionIdsToStages")
            else None,
        )


@dataclass
class SecretLabel:
    key: str
    value: str
    is_safe: bool = True
    flagged_reasons: list = field(default_factory=list)


@dataclass
class LabelSafetyReport:
    secret_id: str
    labels: list = field(default_factory=list)
    overall_safe: bool = True
    unsafe_labels: list = field(default_factory=list)
    checked_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditEmbedding:
    secret_id: str
    audit_notes: str
    embedding: list = field(default_factory=list)
    model: str = ""
    dimension: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str = ""
    target_language: str = ""
    model: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_secret_payload(raw_value: Any) -> dict:
    if isinstance(raw_value, str):
        try:
            return json.loads(raw_value)
        except (json.JSONDecodeError, TypeError):
            return {"raw_secret": raw_value}
    if isinstance(raw_value, bytes):
        try:
            return json.loads(raw_value.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"raw_secret": raw_value.decode("utf-8", errors="replace")}
    if isinstance(raw_value, dict):
        return raw_value
    return {"raw_secret": str(raw_value)}


def build_aws_secret_request(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> SecretRequest:
    return SecretRequest(
        secret_id=secret_id,
        version_id=version_id,
        version_stage=version_stage,
        region=region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
