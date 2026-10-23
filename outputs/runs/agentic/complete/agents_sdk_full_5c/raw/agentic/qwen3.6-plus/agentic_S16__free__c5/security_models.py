"""
security_models.py - Define local request, response, and normalization helpers for Secret Management.

Provides Pydantic models and utilities for secret metadata, rotation tracking,
audit notes, and response normalization across provider integrations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class SecretRotationStatus(Enum):
    """Enumeration of possible secret rotation states."""
    ACTIVE = "active"
    ROTATING = "rotating"
    PENDING_DELETION = "pending_deletion"
    DEPRECATED = "deprecated"
    UNKNOWN = "unknown"


@dataclass
class SecretMetadata:
    """Core metadata associated with a managed secret."""
    secret_id: str
    name: str
    description: str = ""
    labels: List[str] = field(default_factory=list)
    rotation_enabled: bool = False
    rotation_lambda_arn: Optional[str] = None
    rotation_interval_days: int = 0
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    status: SecretRotationStatus = SecretRotationStatus.ACTIVE
    version_ids: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class SecretVersionInfo:
    """Information about a specific secret version or staged value."""
    version_id: str
    stage: str
    created_date: Optional[datetime] = None
    is_current: bool = False
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None


@dataclass
class SecretResponse:
    """Normalized response wrapper for secret retrieval operations."""
    success: bool
    secret_id: str
    secret_value: Optional[str] = None
    secret_value_bytes: Optional[bytes] = None
    version_id: Optional[str] = None
    stage: Optional[str] = None
    metadata: Optional[SecretMetadata] = None
    version_info: Optional[SecretVersionInfo] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to a dictionary representation."""
        result = asdict(self)
        if isinstance(result.get("metadata"), SecretMetadata):
            result["metadata"] = asdict(result["metadata"])
        if isinstance(result.get("version_info"), SecretVersionInfo):
            result["version_info"] = asdict(result["version_info"])
        # Handle datetime serialization
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result


@dataclass
class RotationSummary:
    """Summary of secret rotation status for reporting."""
    secret_id: str
    secret_name: str
    current_status: SecretRotationStatus
    last_rotation: Optional[datetime] = None
    next_rotation: Optional[datetime] = None
    rotation_history: List[Dict[str, Any]] = field(default_factory=list)
    is_overdue: bool = False
    days_since_last_rotation: Optional[int] = None
    recommended_action: str = ""


@dataclass
class AuditNote:
    """Audit note associated with a secret operation."""
    note_id: str
    secret_id: str
    timestamp: datetime
    operation: str
    operator: str
    note_text: str
    labels: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    similarity_score: Optional[float] = None


@dataclass
class SafetyCheckResult:
    """Result of safety analysis on secret labels or notes."""
    secret_id: str
    checked_text: str
    is_safe: bool
    flagged_terms: List[str] = field(default_factory=list)
    confidence: float = 0.0
    explanation: str = ""


def normalize_datetime(dt_value: Any) -> Optional[datetime]:
    """Normalize various datetime representations to a datetime object."""
    if dt_value is None:
        return None
    if isinstance(dt_value, datetime):
        if dt_value.tzinfo is None:
            return dt_value.replace(tzinfo=timezone.utc)
        return dt_value
    if isinstance(dt_value, (int, float)):
        return datetime.fromtimestamp(dt_value, tz=timezone.utc)
    if isinstance(dt_value, str):
        try:
            return datetime.fromisoformat(dt_value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def normalize_secret_value(raw_value: Any) -> str:
    """Normalize a secret value to string format."""
    if raw_value is None:
        return ""
    if isinstance(raw_value, bytes):
        return raw_value.decode("utf-8", errors="replace")
    if isinstance(raw_value, dict) or isinstance(raw_value, list):
        return json.dumps(raw_value, default=str)
    return str(raw_value)


def parse_json_secret_value(secret_string: str) -> Dict[str, Any]:
    """Parse a JSON-formatted secret string into a dictionary."""
    if not secret_string:
        return {}
    try:
        parsed = json.loads(secret_string)
        if isinstance(parsed, dict):
            return parsed
        return {"value": parsed}
    except (json.JSONDecodeError, TypeError):
        return {"raw": secret_string}
