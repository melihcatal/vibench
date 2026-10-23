"""
Local request, response, and normalization helpers for Secret Management.
Defines dataclasses and utility functions for structured secret payloads,
version metadata, and response normalization.
"""

import json
import base64
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List


@dataclass
class SecretVersionInfo:
    """Metadata about a single secret version."""

    version_id: str
    version_stages: List[str] = field(default_factory=list)
    created_date: Optional[datetime] = None
    last_accessed_date: Optional[datetime] = None
    status: str = "unknown"


@dataclass
class SecretResponse:
    """Normalized response returned after fetching a secret."""

    name: str
    arn: str = ""
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None
    version_id: str = ""
    version_stages: List[str] = field(default_factory=list)
    created_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecretRotationStatus:
    """Summarized rotation status for a single secret."""

    name: str
    arn: str
    rotation_enabled: bool = False
    rotation_lambda_arn: str = ""
    rotation_rules: Dict[str, Any] = field(default_factory=dict)
    last_rotated_date: Optional[datetime] = None
    last_changed_date: Optional[datetime] = None
    current_version_id: str = ""
    next_rotation_date: Optional[datetime] = None


@dataclass
class SecretLabelCheck:
    """Result of a safety/label check on secret metadata."""

    name: str
    label: str = ""
    description: str = ""
    is_safe: bool = True
    flagged_terms: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class AuditEmbeddingResult:
    """Result from embedding secret audit notes."""

    secret_name: str
    note_text: str
    embedding: List[float] = field(default_factory=list)
    model: str = ""
    token_count: int = 0


def normalize_secret_response(raw: Dict[str, Any], secret_name: str) -> SecretResponse:
    """
    Normalize a raw AWS Secrets Manager GetSecretValue response
    into a SecretResponse dataclass.
    """
    resp = SecretResponse(
        name=secret_name,
        arn=raw.get("ARN", ""),
        secret_string=raw.get("SecretString"),
        version_id=raw.get("VersionId", ""),
        version_stages=raw.get("VersionStages", []),
        created_date=raw.get("CreatedDate"),
        metadata={},
    )
    if "SecretBinary" in raw:
        resp.secret_binary = raw["SecretBinary"]
    return resp


def normalize_rotation_status(raw: Dict[str, Any]) -> SecretRotationStatus:
    """Normalize a raw DescribeSecret response into a SecretRotationStatus."""
    rules = raw.get("RotationRules", {})
    return SecretRotationStatus(
        name=raw.get("Name", ""),
        arn=raw.get("ARN", ""),
        rotation_enabled=raw.get("RotationEnabled", False),
        rotation_lambda_arn=raw.get("RotationLambdaARN", ""),
        rotation_rules=rules,
        last_rotated_date=raw.get("LastRotatedDate"),
        last_changed_date=raw.get("LastChangedDate"),
        current_version_id=raw.get("VersionIdsToStages", {}),
        next_rotation_date=None,
    )


def parse_secret_json(secret_string: str) -> Dict[str, Any]:
    """
    Parse a JSON-formatted secret string and return the resulting dict.
    Raises ValueError on invalid JSON.
    """
    if not secret_string:
        raise ValueError("Empty secret string")
    try:
        return json.loads(secret_string)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Secret is not valid JSON: {exc}") from exc


def secret_to_dict(response: SecretResponse) -> Dict[str, Any]:
    """Convert a SecretResponse to a plain dictionary, omitting binary data."""
    data = asdict(response)
    if data.get("secret_binary") is not None:
        data["secret_binary"] = base64.b64encode(data["secret_binary"]).decode("utf-8")
    return data
