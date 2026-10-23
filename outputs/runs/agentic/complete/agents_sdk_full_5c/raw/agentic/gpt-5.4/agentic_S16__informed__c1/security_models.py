from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional
import json


@dataclass
class SecretReference:
    project_id: str
    secret_id: str
    version_id: str = "latest"

    @property
    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"


@dataclass
class SecretPayload:
    name: str
    value: str
    version_id: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def json(self) -> Any:
        return json.loads(self.value)


@dataclass
class RotationSummary:
    secret_name: str
    version_count: int
    enabled_versions: List[str]
    disabled_versions: List[str]
    latest_version: Optional[str]
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class SafetyFinding:
    text: str
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    model: str
    vector: List[float]
    dimensions: int


@dataclass
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str


def normalize_secret_labels(labels: Optional[Mapping[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (labels or {}).items()}


def parse_secret_json(secret_value: str) -> Dict[str, Any]:
    data = json.loads(secret_value)
    if not isinstance(data, dict):
        raise ValueError("Secret payload must decode to a JSON object")
    return data


def parse_version_id(resource_name: str) -> Optional[str]:
    parts = resource_name.split("/")
    if len(parts) >= 2 and parts[-2] == "versions":
        return parts[-1]
    return None
