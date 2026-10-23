from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union


SecretValue = Union[str, Dict[str, Any], list]


@dataclass(frozen=True)
class SecretFetchRequest:
    secret_id: str
    version: str = "latest"
    project_id: str = ""


@dataclass(frozen=True)
class SecretFetchResponse:
    secret_id: str
    version: str
    project_id: str
    value: SecretValue
    provider: str


@dataclass(frozen=True)
class SecretRotationRequest:
    secret_id: str
    payload: str
    version_alias: str = "latest"
    project_id: str = ""


@dataclass(frozen=True)
class SecretRotationResponse:
    secret_id: str
    project_id: str
    version_name: str
    staged_value: str
    provider: str


@dataclass(frozen=True)
class SecretAnalysisRequest:
    label: str
    notes: str
    provider: str = "google-cloud-secret-manager"


@dataclass(frozen=True)
class SecretAnalysisResponse:
    risk_level: str
    summary: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_secret_payload(payload: Any) -> Any:
    if isinstance(payload, bytes):
        return payload.decode("utf-8")
    if isinstance(payload, str):
        return payload.strip()
    return payload
