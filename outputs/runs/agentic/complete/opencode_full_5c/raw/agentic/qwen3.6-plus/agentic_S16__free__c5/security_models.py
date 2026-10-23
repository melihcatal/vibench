import os
import json
from typing import Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = "AWSCURRENT"
    region: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    secret_value: str
    version_id: str
    version_stage: str
    arn: str
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RotationStatus:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: dict = field(default_factory=dict)
    current_version: Optional[str] = None
    pending_version: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditNote:
    secret_id: str
    note_text: str
    timestamp: Optional[str] = None
    labels: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ParsedSecret:
    secret_id: str
    parsed_data: dict
    raw_value: str
    version_id: str

    def to_dict(self) -> dict:
        return {
            "secret_id": self.secret_id,
            "parsed_data": self.parsed_data,
            "version_id": self.version_id,
        }


@dataclass
class SafetyCheckResult:
    secret_id: str
    is_safe: bool
    flagged_items: list = field(default_factory=list)
    confidence: float = 0.0
    details: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EmbeddingResult:
    secret_id: str
    embedding: list
    model: str
    text_length: int

    def to_dict(self) -> dict:
        return {
            "secret_id": self.secret_id,
            "model": self.model,
            "text_length": self.text_length,
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    model: str

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_aws_secret_response(raw_response: dict) -> SecretResponse:
    secret_value = raw_response.get("SecretString", "")
    if not secret_value and "SecretBinary" in raw_response:
        import base64

        secret_value = base64.b64decode(raw_response["SecretBinary"]).decode("utf-8")

    return SecretResponse(
        secret_id=raw_response.get("Name", ""),
        secret_value=secret_value,
        version_id=raw_response.get("VersionId", ""),
        version_stage=raw_response.get("VersionStage", ["AWSCURRENT"])[0]
        if isinstance(raw_response.get("VersionStage"), list)
        else raw_response.get("VersionStage", "AWSCURRENT"),
        arn=raw_response.get("ARN", ""),
        metadata={
            k: v
            for k, v in raw_response.items()
            if k
            not in (
                "Name",
                "SecretString",
                "SecretBinary",
                "VersionId",
                "VersionStage",
                "ARN",
            )
        },
    )


def normalize_aws_rotation_response(raw_response: dict) -> RotationStatus:
    rotation_rules = raw_response.get("RotationRules", {})
    return RotationStatus(
        secret_id=raw_response.get("Name", ""),
        rotation_enabled=raw_response.get("RotationEnabled", False),
        last_rotated_date=raw_response.get("LastRotatedDate"),
        next_rotation_date=raw_response.get("NextRotationDate"),
        rotation_lambda_arn=raw_response.get("RotationLambdaARN"),
        rotation_rules={
            "automatically_after_days": rotation_rules.get("AutomaticallyAfterDays"),
        },
        current_version=raw_response.get("CurrentVersionId"),
        pending_version=raw_response.get("NextRotationDate"),
    )


def normalize_aws_describe_response(raw_response: dict) -> dict:
    return {
        "arn": raw_response.get("ARN", ""),
        "name": raw_response.get("Name", ""),
        "description": raw_response.get("Description", ""),
        "rotation_enabled": raw_response.get("RotationEnabled", False),
        "rotation_lambda_arn": raw_response.get("RotationLambdaARN"),
        "last_rotated_date": raw_response.get("LastRotatedDate"),
        "next_rotation_date": raw_response.get("NextRotationDate"),
        "tags": raw_response.get("Tags", []),
        "version_ids_to_stages": raw_response.get("VersionIdsToStages", {}),
    }
