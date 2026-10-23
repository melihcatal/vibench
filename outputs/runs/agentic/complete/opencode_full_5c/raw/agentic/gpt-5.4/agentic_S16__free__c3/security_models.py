from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class SecretReference:
    project_id: str
    secret_id: str
    version_id: str = "latest"

    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"


@dataclass(frozen=True)
class SecretPayload:
    name: str
    value: str
    version_id: str
    labels: Dict[str, str]
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class RotationSummary:
    secret_name: str
    version_count: int
    latest_enabled_version: Optional[str]
    has_scheduled_rotation: bool
    labels: Dict[str, str]


def decode_secret_bytes(payload_bytes: bytes) -> str:
    return payload_bytes.decode("utf-8")


def parse_json_secret_value(secret_value: str) -> Dict[str, Any]:
    parsed = json.loads(secret_value)
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON secret to decode to an object")
    return parsed


def normalize_labels(labels: Optional[Dict[str, str]]) -> Dict[str, str]:
    return dict(sorted((labels or {}).items()))


def flatten_label_text(labels: Dict[str, str], notes: Optional[str] = None) -> str:
    label_text = " ".join(
        f"{key}:{value}" for key, value in normalize_labels(labels).items()
    )
    return " ".join(part for part in [label_text, notes or ""] if part).strip()


def enabled_version_numbers(versions: Iterable[Any]) -> List[str]:
    enabled = []
    for version in versions:
        state_name = getattr(getattr(version, "state", None), "name", "")
        if state_name == "ENABLED":
            enabled.append(version.name.rsplit("/", 1)[-1])
    return enabled
