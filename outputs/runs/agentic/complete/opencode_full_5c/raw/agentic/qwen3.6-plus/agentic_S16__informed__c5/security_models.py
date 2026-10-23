import os
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class SecretType(Enum):
    API_KEY = "api_key"
    DATABASE = "database"
    JSON_CONFIG = "json_config"
    GENERIC = "generic"


@dataclass
class SecretRequest:
    secret_id: str
    secret_type: SecretType = SecretType.GENERIC
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    region: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    secret_value: str
    secret_type: SecretType = SecretType.GENERIC
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    created_date: Optional[str] = None
    last_rotated_date: Optional[str] = None
    rotation_enabled: bool = False
    metadata: dict = field(default_factory=dict)

    def parsed_json(self) -> dict:
        import json

        return json.loads(self.secret_value)


@dataclass
class RotationStatus:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    current_version_id: Optional[str] = None
    pending_version_id: Optional[str] = None
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: dict = field(default_factory=dict)
    version_stages: dict = field(default_factory=dict)
    notes: str = ""


@dataclass
class AuditNote:
    secret_id: str
    note_text: str
    timestamp: Optional[str] = None
    author: Optional[str] = None
    embedding: Optional[list] = None


@dataclass
class RunbookNote:
    note_id: str
    source_text: str
    source_language: str = "en"
    target_language: str = "en"
    translated_text: Optional[str] = None


@dataclass
class SafetyCheckResult:
    text: str
    is_safe: bool
    categories: dict
    severity_scores: dict
    flagged_terms: list = field(default_factory=list)


def normalize_secret_name(raw_name: str) -> str:
    return raw_name.strip().lower().replace("_", "-")


def normalize_region(region: Optional[str]) -> str:
    if region:
        return region.strip()
    return os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def build_version_specifier(
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> dict:
    specifier = {}
    if version_id:
        specifier["VersionId"] = version_id
    if version_stage:
        specifier["VersionStage"] = version_stage
    return specifier


def format_rotation_summary(status: RotationStatus) -> str:
    lines = [
        f"Secret: {status.secret_id}",
        f"Rotation Enabled: {status.rotation_enabled}",
        f"Last Rotated: {status.last_rotated_date or 'Never'}",
        f"Next Rotation: {status.next_rotation_date or 'Not scheduled'}",
        f"Current Version: {status.current_version_id or 'Unknown'}",
        f"Pending Version: {status.pending_version_id or 'None'}",
        f"Rotation Lambda: {status.rotation_lambda_arn or 'Not configured'}",
    ]
    if status.rotation_rules:
        lines.append(f"Rotation Rules: {status.rotation_rules}")
    if status.version_stages:
        lines.append(f"Version Stages: {status.version_stages}")
    if status.notes:
        lines.append(f"Notes: {status.notes}")
    return "\n".join(lines)
