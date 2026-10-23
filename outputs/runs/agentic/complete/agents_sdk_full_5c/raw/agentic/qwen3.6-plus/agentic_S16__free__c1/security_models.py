"""
security_models.py - Local request, response, and normalization helpers for Secret Management.

Provides dataclasses and utilities for normalizing secret responses,
handling version metadata, and structuring rotation and audit payloads.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class SecretVersionInfo:
    """Metadata for a single secret version."""
    version_id: str
    version_stages: List[str] = field(default_factory=list)
    created_date: Optional[str] = None
    last_accessed_date: Optional[str] = None

    @classmethod
    def from_aws_response(cls, version_data: Dict[str, Any]) -> "SecretVersionInfo":
        created = version_data.get("CreatedDate")
        if isinstance(created, datetime):
            created = created.isoformat()
        accessed = version_data.get("LastAccessedDate")
        if isinstance(accessed, datetime):
            accessed = accessed.isoformat()
        return cls(
            version_id=version_data.get("VersionId", ""),
            version_stages=version_data.get("VersionStages", []),
            created_date=created,
            last_accessed_date=accessed,
        )


@dataclass
class SecretResponse:
    """Normalized response for a fetched secret."""
    name: str
    arn: str
    value: str
    version_id: str
    version_stages: List[str] = field(default_factory=list)
    created_date: Optional[str] = None
    last_rotated_date: Optional[str] = None
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None
    raw_metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_aws_response(cls, get_secret_value_resp: Dict[str, Any], metadata: Dict[str, Any]) -> "SecretResponse":
        last_rotated = metadata.get("LastRotatedDate")
        if isinstance(last_rotated, datetime):
            last_rotated = last_rotated.isoformat()
        return cls(
            name=metadata.get("Name", ""),
            arn=metadata.get("ARN", ""),
            value=get_secret_value_resp.get("SecretString", "") or get_secret_value_resp.get("SecretBinary", ""),
            version_id=get_secret_value_resp.get("VersionId", ""),
            version_stages=get_secret_value_resp.get("VersionStages", []),
            created_date=metadata.get("CreatedDate", ""),
            last_rotated_date=last_rotated,
            rotation_enabled=metadata.get("RotationEnabled", False),
            rotation_lambda_arn=metadata.get("RotationLambdaARN"),
            raw_metadata=metadata,
        )


@dataclass
class RotationStatus:
    """Summarized rotation status for a secret."""
    secret_name: str
    arn: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str]
    last_rotated_date: Optional[str]
    next_rotation_date: Optional[str]
    automatic_rotation_days: Optional[int]
    current_version: str
    staged_versions: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditNotePayload:
    """Payload for secret audit embedding."""
    secret_name: str
    audit_note: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


@dataclass
class SafetyCheckResult:
    """Result of a label/note safety check."""
    secret_name: str
    is_safe: bool
    confidence: float = 0.0
    flagged_terms: List[str] = field(default_factory=list)
    explanation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    """Result of translating runbook notes."""
    source_text: str
    translated_text: str
    source_language: str = "en"
    target_language: str = "en"
    provider: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_secret_name(raw_name: str) -> str:
    """Normalize a secret name by stripping whitespace and converting slashes."""
    return raw_name.strip().replace("\\", "/")


def parse_secret_value_as_json(value: str) -> Dict[str, Any]:
    """Parse a secret string value as JSON, returning empty dict on failure."""
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}
