from __future__ import annotations
import typing as t


class SecretPayload(t.TypedDict):
    """Normalized secret payload structure used internally."""

    value: str
    metadata: t.Dict[str, str]


class SecretRotationStatus(t.TypedDict):
    """Structure returned by rotation_summary."""

    secret_name: str
    current_version: str
    staged_version: t.Optional[str]
    rotated: bool
    error: t.Optional[str]


class LabelSafetyCheck(t.TypedDict):
    """Result of secret_label_safety check."""

    labels: t.List[str]
    unsafe: t.List[str]
    safe: t.List[str]


class EmbeddingRequest(t.TypedDict):
    """Payload for secret_audit_embedding."""

    notes: str
    secret_name: str

    # Provider-specific metadata can be added here if needed


class RunbookTranslation(t.TypedDict):
    """Result of runbook_translate."""

    original: str
    translated: str
    provider_hint: t.Optional[str]
