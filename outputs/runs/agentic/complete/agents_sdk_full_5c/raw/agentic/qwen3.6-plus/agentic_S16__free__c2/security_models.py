"""Local request, response, and normalization helpers for Secret Management."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class SecretRequest:
    """Normalized request for fetching a secret."""
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    include_metadata: bool = True


@dataclass
class SecretResponse:
    """Normalized response after fetching a secret."""
    secret_id: str
    secret_value: str
    version_id: Optional[str] = None
    version_stages: Optional[List[str]] = None
    created_date: Optional[datetime] = None
    rotation_enabled: bool = False
    last_rotated_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RotationStatus:
    """Normalized rotation status for a secret."""
    secret_id: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    current_version_id: Optional[str] = None
    versions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SecretLabel:
    """Represents a secret with label and notes."""
    secret_id: str
    labels: Dict[str, str]
    description: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class AuditNote:
    """Represents an audit note for a secret operation."""
    secret_id: str
    operation: str
    timestamp: datetime
    note_text: str
    operator: Optional[str] = None
    status: str = "completed"


@dataclass
class RunbookNote:
    """Represents a runbook note for secret rotation procedures."""
    procedure_name: str
    original_language: str
    target_language: str
    note_text: str
    steps: List[str] = field(default_factory=list)


def normalize_secret_response(raw_response: Dict[str, Any]) -> SecretResponse:
    """Normalize a raw provider response into a SecretResponse."""
    secret_value = raw_response.get("SecretString", raw_response.get("SecretBinary", ""))
    if isinstance(secret_value, bytes):
        secret_value = secret_value.decode("utf-8")

    return SecretResponse(
        secret_id=raw_response.get("Name", ""),
        secret_value=secret_value,
        version_id=raw_response.get("VersionId"),
        version_stages=raw_response.get("VersionStages"),
        created_date=raw_response.get("CreatedDate"),
        rotation_enabled=raw_response.get("RotationEnabled", False),
        last_rotated_date=raw_response.get("LastRotatedDate"),
        metadata={
            "arn": raw_response.get("ARN", ""),
            "description": raw_response.get("Description", ""),
        },
    )


def normalize_rotation_status(raw_metadata: Dict[str, Any]) -> RotationStatus:
    """Normalize raw secret metadata into a RotationStatus."""
    return RotationStatus(
        secret_id=raw_metadata.get("Name", ""),
        rotation_enabled=raw_metadata.get("RotationEnabled", False),
        rotation_lambda_arn=raw_metadata.get("RotationLambdaARN"),
        rotation_rules=raw_metadata.get("RotationRules"),
        last_rotated_date=raw_metadata.get("LastRotatedDate"),
        next_rotation_date=raw_metadata.get("NextRotationDate"),
        current_version_id=raw_metadata.get("CurrentVersionId"),
        versions=[
            {
                "version_id": v.get("VersionId", ""),
                "version_stages": v.get("VersionStages", []),
                "created_date": v.get("CreatedDate"),
            }
            for v in raw_metadata.get("VersionIdsToStages", {})
        ],
    )


def parse_json_secret_value(secret_value: str) -> Dict[str, Any]:
    """Parse a JSON-formatted secret string into a dictionary."""
    import json
    return json.loads(secret_value)
