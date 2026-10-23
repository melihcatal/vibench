from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import json


@dataclass
class SecretLocator:
    project_id: str
    secret_id: str
    version_id: str = "latest"

    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"


@dataclass
class SecretPayload:
    name: str
    value: str

    def as_json(self) -> dict[str, Any]:
        return json.loads(self.value)


@dataclass
class RotationSummary:
    secret_name: str
    version_name: str
    state: str
    create_time: str
    destroy_time: str | None
    labels: dict[str, str]


def normalize_text(value: str | None) -> str:
    return (value or "").strip()


def normalize_labels(labels: dict[str, str] | None) -> dict[str, str]:
    return {str(k): str(v) for k, v in (labels or {}).items()}


def flatten_secret_notes(labels: dict[str, str], notes: str | None = None) -> str:
    ordered = [
        f"{key}:{value}" for key, value in sorted(normalize_labels(labels).items())
    ]
    if notes:
        ordered.append(normalize_text(notes))
    return " | ".join(part for part in ordered if part)
