from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping, Optional
import json


@dataclass(frozen=True)
class SecretName:
    value: str

    def normalized(self) -> str:
        return self.value.strip()


@dataclass(frozen=True)
class SecretPayload:
    name: str
    value: str
    version: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NormalizedSecret:
    name: str
    text: str
    parsed_json: Optional[dict[str, Any]] = None

    def to_json(self) -> str:
        return json.dumps({"name": self.name, "text": self.text, "parsed_json": self.parsed_json}, ensure_ascii=False)


@dataclass(frozen=True)
class RotationStatus:
    secret_name: str
    active_version: Optional[str]
    previous_version: Optional[str]
    staged_version: Optional[str]
    description: str = ""


@dataclass(frozen=True)
class SafetyFinding:
    label: str
    unsafe: bool
    reason: str
    source: str = "Azure AI Content Safety"


@dataclass(frozen=True)
class AuditEmbedding:
    note: str
    vector: list[float]
    model: str


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None


def coerce_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if hasattr(value, "dict"):
        return dict(value.dict())
    raise TypeError(f"Unsupported mapping type: {type(value)!r}")
