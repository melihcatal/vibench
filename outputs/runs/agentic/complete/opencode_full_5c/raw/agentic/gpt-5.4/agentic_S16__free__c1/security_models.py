from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SecretFetchRequest:
    project_id: str
    secret_id: str
    version_id: str = "latest"


@dataclass
class SecretVersionSelection:
    project_id: str
    secret_id: str
    version_id: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretValue:
    provider: str
    resource_name: str
    value: str
    version: str


@dataclass
class RotationSummary:
    secret_name: str
    latest_version: str
    state: str
    label_count: int
    next_rotation_time: Optional[str]
    notes: str


@dataclass
class SafetyCheckResult:
    resource_name: str
    unsafe: bool
    findings: List[str]


def normalize_secret_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def normalize_labels(labels: Optional[Dict[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (labels or {}).items()}


def normalize_rotation_state(state: Any) -> str:
    if state is None:
        return "UNKNOWN"
    return str(state).split(".")[-1].upper()
