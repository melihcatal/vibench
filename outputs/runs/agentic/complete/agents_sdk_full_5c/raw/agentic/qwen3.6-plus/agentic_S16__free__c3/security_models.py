"""
Local request, response, and normalization helpers for Secret Management.

Defines data classes and helper functions for structured secret management
operations across AWS Secrets Manager integrations.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SecretFetchResult:
    """Result of a secret fetch operation."""

    success: bool
    secret_name: str
    provider: str
    secret_value: Optional[str] = None
    secret_data: Optional[Dict[str, Any]] = None
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    arn: Optional[str] = None
    error: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class DatabaseCredentials:
    """Parsed database credentials from a secret."""

    engine: str
    username: str
    password: str
    host: str
    port: int
    database: str
    provider: str
    version_id: Optional[str] = None
    ssl_mode: Optional[str] = None
    extra_params: Optional[Dict[str, str]] = None


@dataclass
class SecretVersionInfo:
    """Information about a specific secret version."""

    version_id: str
    stages: List[str]
    secret_name: str
    provider: str
    created_date: Optional[str] = None


@dataclass
class SecretRotationStatus:
    """Status information for secret rotation."""

    secret_name: str
    provider: str
    rotation_enabled: bool
    rotation_lambda_arn: Optional[str] = None
    rotation_rules: Optional[Dict[str, Any]] = None
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
    current_version_stage: Optional[str] = None
    pending_version_stage: Optional[str] = None


@dataclass
class SecretLabelCheckResult:
    """Result of a label safety check."""

    secret_name: str
    provider: str
    is_safe: bool
    unsafe_fields: List[str] = field(default_factory=list)
    unsafe_patterns: List[str] = field(default_factory=list)


def normalize_secret_payload(raw_value: str) -> Optional[Dict[str, Any]]:
    """
    Normalize a raw secret string into a structured dictionary.

    Args:
        raw_value: The raw secret string (expected JSON).

    Returns:
        Parsed dictionary or None if parsing fails.
    """
    import json

    try:
        data = json.loads(raw_value)
        if isinstance(data, dict):
            return data
        return {"value": data}
    except (json.JSONDecodeError, ValueError):
        return None


def redact_secret_value(value: str, visible_chars: int = 4) -> str:
    """
    Redact a secret value for logging or display.

    Args:
        value: The secret value to redact.
        visible_chars: Number of characters to keep visible.

    Returns:
        Redacted string.
    """
    if not value or len(value) <= visible_chars:
        return "****"
    return value[:visible_chars] + "*" * (len(value) - visible_chars)
