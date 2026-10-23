"""Local request, response, and normalization helpers for Secret Management.

Defines dataclasses for secret fetch requests and responses used across
the integration files.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SecretFetchRequest:
    """Describes a request to fetch a secret."""

    secret_name: str
    version_id: str | None = None
    version_stage: str = "AWSCURRENT"
    provider: str = "aws_secrets_manager"


@dataclass
class SecretFetchResponse:
    """Represents the result of a secret fetch operation."""

    secret_name: str
    secret_value: str | None = None
    version_id: str | None = None
    error: str | None = None
    metadata: dict[str, Any] | None = None
    provider: str = "aws_secrets_manager"

    @property
    def is_success(self) -> bool:
        return self.error is None

    def to_dict(self) -> dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "version_id": self.version_id,
            "provider": self.provider,
            "has_value": self.secret_value is not None,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class SecretVersionInfo:
    """Metadata about a specific secret version."""

    version_id: str
    stages: list[str] = field(default_factory=list)
    created_date: str | None = None

    @property
    def is_current(self) -> bool:
        return "AWSCURRENT" in self.stages

    @property
    def is_pending(self) -> bool:
        return "AWSPENDING" in self.stages
