"""Define local request, response, and normalization helpers for Secret Management.

Provides dataclasses and utilities for structured secret data handling
with AWS Secrets Manager integration responses.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class SecretFetchResult:
    """Normalized response from a secret fetch operation.

    Attributes:
        secret_id: The identifier of the secret in the provider store.
        secret_value: The raw secret string value.
        version_id: The version identifier from the provider.
        version_stages: List of staging labels (e.g., AWSCURRENT, AWSPENDING).
        created_date: Timestamp when this version was created.
        provider: The provider name (e.g., aws_secrets_manager).
    """

    secret_id: str
    secret_value: str
    version_id: str = ""
    version_stages: list[str] = field(default_factory=list)
    created_date: Optional[datetime] = None
    provider: str = "aws_secrets_manager"

    def to_dict(self) -> dict:
        """Convert to a serializable dictionary."""
        return {
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "version_stages": self.version_stages,
            "provider": self.provider,
        }


@dataclass
class SecretError(Exception):
    """Custom error for secret management operations.

    Attributes:
        secret_id: The secret that caused the error.
        message: Human-readable error message.
        error_code: Provider-specific error code (e.g., ResourceNotFoundException).
        provider: The provider that raised the error.
    """

    secret_id: str
    message: str
    error_code: str = "UNKNOWN"
    provider: str = "aws_secrets_manager"

    def __str__(self) -> str:
        return f"[{self.provider}] {self.secret_id}: {self.message} ({self.error_code})"


@dataclass
class RotationStatus:
    """Normalized rotation status for a secret.

    Attributes:
        secret_id: The secret identifier.
        rotation_enabled: Whether automatic rotation is enabled.
        rotation_lambda_arn: ARN of the Lambda function performing rotation.
        rotation_rules: Dict with AutomaticallyAfterDays and other rules.
        last_rotated_date: When the secret was last rotated.
        next_rotation_date: Scheduled next rotation date.
        current_version: The current AWSCURRENT version ID.
        pending_version: The AWSPENDING version ID if rotation is in progress.
        provider: The provider name.
    """

    secret_id: str
    rotation_enabled: bool = False
    rotation_lambda_arn: str = ""
    rotation_rules: dict[str, Any] = field(default_factory=dict)
    last_rotated_date: Optional[datetime] = None
    next_rotation_date: Optional[datetime] = None
    current_version: str = ""
    pending_version: str = ""
    provider: str = "aws_secrets_manager"


@dataclass
class SecretLabel:
    """Represents a secret label or tag with metadata.

    Attributes:
        key: The label key.
        value: The label value.
        secret_id: The associated secret identifier.
        notes: Additional notes or description attached to the label.
    """

    key: str
    value: str
    secret_id: str
    notes: str = ""


@dataclass
class AuditNote:
    """Represents an audit note for a secret operation.

    Attributes:
        secret_id: The secret the audit note relates to.
        action: The action performed (e.g., ROTATE, READ, UPDATE).
        timestamp: When the action occurred.
        notes: Free-form audit notes text.
        operator: Who performed the action.
    """

    secret_id: str
    action: str
    timestamp: datetime
    notes: str
    operator: str = "system"


def normalize_secret_value(value: Any) -> str:
    """Normalize a secret value to a string, handling bytes and dicts."""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, dict):
        import json
        return json.dumps(value)
    return str(value)


def mask_secret_value(value: str, visible_chars: int = 4) -> str:
    """Mask a secret value for safe logging or display.

    Shows only the first visible_chars characters, replacing the rest with asterisks.
    """
    if len(value) <= visible_chars:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars)
