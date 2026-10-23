"""Local request, response, and normalization helpers for Secret Management.

Defines dataclasses and normalization utilities for secret retrieval,
rotation events, and audit metadata across providers.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SecretFetchRequest:
    """Normalized request for fetching a secret."""

    secret_name: str
    provider: str
    version: str | None = None
    project: str | None = None
    config: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class SecretFetchResponse:
    """Normalized response from a secret fetch operation."""

    name: str
    value: str | None
    version: str | None
    provider: str
    staged: bool = False
    retrieved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_stale(self, max_age_seconds: float = 300) -> bool:
        """Check if the secret response is older than max_age_seconds."""
        age = (datetime.now(timezone.utc) - self.retrieved_at).total_seconds()
        return age > max_age_seconds


@dataclass
class RotationEvent:
    """Represents a secret rotation event."""

    secret_name: str
    provider: str
    old_version: str | None
    new_version: str | None
    rotated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    rotated_by: str = "system"
    status: str = "completed"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "provider": self.provider,
            "old_version": self.old_version,
            "new_version": self.new_version,
            "rotated_at": self.rotated_at.isoformat(),
            "rotated_by": self.rotated_by,
            "status": self.status,
            "notes": self.notes,
        }


@dataclass
class AuditNote:
    """An audit note associated with a secret operation."""

    secret_name: str
    action: str
    note_text: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    labels: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "action": self.action,
            "note_text": self.note_text,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
        }


def normalize_version_string(version: Any) -> str | None:
    """Normalize a version identifier to a string or None."""
    if version is None:
        return None
    if isinstance(version, str):
        return version.strip() or None
    return str(version)


def build_secret_path(provider: str, secret_name: str, **kwargs: Any) -> str:
    """Build a provider-specific secret path identifier for logging/audit."""
    if provider == "aws":
        region = kwargs.get("region", "us-east-1")
        return f"arn:aws:secretsmanager:{region}:*:secret:{secret_name}"
    if provider == "azure":
        vault = kwargs.get("vault_url", "unknown")
        return f"{vault}/secrets/{secret_name}"
    if provider == "gcp":
        project = kwargs.get("project_id", "unknown")
        return f"projects/{project}/secrets/{secret_name}"
    if provider == "doppler":
        project = kwargs.get("project", "unknown")
        config = kwargs.get("config", "prod")
        return f"doppler://{project}/{config}/{secret_name}"
    return f"{provider}://{secret_name}"
