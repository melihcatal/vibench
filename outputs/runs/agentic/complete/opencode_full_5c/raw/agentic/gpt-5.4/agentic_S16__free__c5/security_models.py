from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import json


@dataclass
class SecretRequest:
    project_id: str
    secret_id: str
    version_id: str = "latest"


@dataclass
class ParsedSecret:
    name: str
    value: str
    version: str
    labels: dict[str, str] = field(default_factory=dict)
    annotations: dict[str, Any] = field(default_factory=dict)


@dataclass
class RotationSummary:
    secret_name: str
    version: str
    state: str
    labels: dict[str, str]


def parse_secret_json(secret_value: str) -> dict[str, Any]:
    return json.loads(secret_value)


def normalize_secret_name(project_id: str, secret_id: str, version_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"


def normalize_rotation_state(version_state: Any) -> str:
    state = str(version_state).split(".")[-1]
    return state.lower()
