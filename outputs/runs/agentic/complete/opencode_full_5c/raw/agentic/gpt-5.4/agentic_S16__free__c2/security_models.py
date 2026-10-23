from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import json


@dataclass
class SecretFetchRequest:
    project_id: str
    secret_id: str
    version_id: str = "latest"


@dataclass
class SecretVersionRequest:
    project_id: str
    secret_id: str
    version_id: str


@dataclass
class SecretPayload:
    project_id: str
    secret_id: str
    version_id: str
    value: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class RotationSummary:
    secret_id: str
    version_id: str
    state: str
    enabled: bool
    labels: dict[str, str] = field(default_factory=dict)


def normalize_secret_resource(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"


def decode_secret_bytes(payload: bytes) -> str:
    return payload.decode("utf-8")


def parse_secret_json(secret_text: str) -> dict[str, Any]:
    parsed = json.loads(secret_text)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON payload must be an object")
    return parsed


def normalize_rotation_state(state: Any) -> str:
    return getattr(state, "name", str(state))


def collect_text_fields(labels: dict[str, str] | None, notes: str | None) -> list[str]:
    parts: list[str] = []
    if labels:
        parts.extend([f"{key}:{value}" for key, value in labels.items()])
    if notes:
        parts.append(notes)
    return parts
