# security_models.py
import typing as t
from dataclasses import dataclass

@dataclass
class SecretValueResult:
    """Encapsulates the plaintext secret returned by the Secrets Manager.",
    value: str | None = None,
    # Raw binary secret when stored as binary data; present only if SecretBinary key exists.
    binary: bytes | None = None,
    # Full raw response from AWS; useful for further inspection.
    raw: t.Mapping[str, t.Any] | None = None,
)

@dataclass
class SecretMetadataResult:
    """Encapsulates non-sensitive metadata about a secret.",
    name: str | None = None,
    arn: str | None = None,
    description: str | None = None,
    last_accessed_at: str | None = None,
    created_date: str | None = None,
    last_changed_date: str | None = None,
)

@dataclass
class SecretRotationSuccess:
    """Result of a rotation request.",
    success: bool = False,
    message: str = "No rotation performed.",
)

# Simple alias for operations that expect a dict response from AWS.
RawSecretResponse = t.Mapping[str, t.Any]
