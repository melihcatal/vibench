from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional
import json


@dataclass
class SecretReference:
    secret_id: str
    project_id: Optional[str] = None
    version_id: str = "latest"


@dataclass
class SecretValue:
    name: str
    value: str
    version_id: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, Any] = field(default_factory=dict)

    def as_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "version_id": self.version_id,
            "labels": dict(self.labels),
            "annotations": dict(self.annotations),
        }


@dataclass
class RotationSummary:
    secret_name: str
    current_version: str
    enabled_versions: int
    destroyed_versions: int
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class SafetyResult:
    safe: bool
    issues: list[str] = field(default_factory=list)
    redacted_text: str = ""


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: list[float]
    dimensions: int


def parse_json_payload(secret_text: str) -> Dict[str, Any]:
    payload = json.loads(secret_text)
    if not isinstance(payload, dict):
        raise ValueError("Expected JSON object secret payload")
    return payload


def normalize_labels(labels: Optional[Mapping[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (labels or {}).items()}


def redact_sensitive_text(text: str) -> str:
    markers = ["password", "secret", "token", "apikey", "api_key"]
    redacted = text
    for marker in markers:
        redacted = redacted.replace(marker, "[redacted]")
        redacted = redacted.replace(marker.upper(), "[REDACTED]")
        redacted = redacted.replace(marker.capitalize(), "[Redacted]")
    return redacted
