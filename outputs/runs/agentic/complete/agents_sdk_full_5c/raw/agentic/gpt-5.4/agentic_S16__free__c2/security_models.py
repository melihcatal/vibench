from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import json


@dataclass(slots=True)
class SecretFetchRequest:
    secret_id: str
    version_id: str = "latest"


@dataclass(slots=True)
class SecretValue:
    secret_id: str
    version_id: str
    value: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_json(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "value": self.value,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class RotationSummary:
    secret_name: str
    current_version: Optional[str]
    pending_version: Optional[str]
    stages: Dict[str, str]


@dataclass(slots=True)
class SafetyCheckResult:
    safe: bool
    findings: list[str]


@dataclass(slots=True)
class EmbeddingRecord:
    text: str
    vector: list[float]
    model: str


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    provider: str


def normalize_secret_string(value: str) -> str:
    return value.strip()


def parse_json_secret_string(value: str) -> Dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object secret payload")
    return parsed


def safe_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return metadata or {}
