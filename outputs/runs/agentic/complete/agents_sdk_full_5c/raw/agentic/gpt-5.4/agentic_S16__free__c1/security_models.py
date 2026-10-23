from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional
import json


@dataclass
class SecretReference:
    project_id: str
    secret_id: str
    version_id: str = "latest"

    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"


@dataclass
class SecretPayload:
    name: str
    data: str
    version_id: str
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, Any] = field(default_factory=dict)

    def as_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "data": self.data,
            "version_id": self.version_id,
            "labels": self.labels,
            "annotations": self.annotations,
        }


@dataclass
class RotationStatus:
    secret_name: str
    current_version: str
    state: str
    labels: Dict[str, str] = field(default_factory=dict)
    notes: Optional[str] = None

    def summary_text(self) -> str:
        label_text = ", ".join(f"{k}={v}" for k, v in sorted(self.labels.items()))
        return f"secret={self.secret_name}; version={self.current_version}; state={self.state}; labels={label_text}; notes={self.notes or ''}".strip()


@dataclass
class SafetyFinding:
    text: str
    unsafe_terms: List[str]
    is_safe: bool


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]


@dataclass
class TranslationResult:
    provider: str
    model: str
    translated_text: str


def decode_secret_bytes(payload_bytes: bytes) -> str:
    return payload_bytes.decode("utf-8")



def parse_json_secret_text(secret_text: str) -> Dict[str, Any]:
    return json.loads(secret_text)



def normalize_labels(labels: Optional[Mapping[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (labels or {}).items()}



def collect_unsafe_terms(text: str, terms: Iterable[str]) -> List[str]:
    lowered = text.lower()
    return [term for term in terms if term.lower() in lowered]
