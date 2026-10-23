from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional
import json


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretRecord:
    secret_id: str
    version_id: Optional[str]
    version_stages: List[str] = field(default_factory=list)
    value: str = ""
    created_date: Optional[str] = None


@dataclass
class RotationSummary:
    secret_id: str
    current_version: Optional[str]
    stages: List[str]
    is_rotation_ready: bool
    summary: str


@dataclass
class SafetyAssessment:
    text: str
    flagged: bool
    categories: Dict[str, float]
    unsafe_terms: List[str]


@dataclass
class EmbeddingVector:
    provider: str
    model: str
    dimensions: int
    vector: List[float]
    input_text: str


@dataclass
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str
    provider: str


def parse_secret_json(secret_value: str) -> Dict[str, Any]:
    return json.loads(secret_value)


def normalize_secret_response(
    secret_id: str, response: Mapping[str, Any]
) -> SecretRecord:
    stages = response.get("VersionStages") or response.get("version_stages") or []
    created = response.get("CreatedDate") or response.get("created_date")
    if created is not None and not isinstance(created, str):
        created = str(created)
    return SecretRecord(
        secret_id=secret_id,
        version_id=response.get("VersionId") or response.get("version_id"),
        version_stages=list(stages),
        value=response.get("SecretString") or response.get("secret_string") or "",
        created_date=created,
    )


def summarize_rotation(secret: SecretRecord) -> RotationSummary:
    ready = (
        "AWSCURRENT" in secret.version_stages or "AWSPENDING" in secret.version_stages
    )
    summary = (
        f"Secret {secret.secret_id} version {secret.version_id or 'unknown'} "
        f"has stages {', '.join(secret.version_stages) or 'none'}"
    )
    return RotationSummary(
        secret_id=secret.secret_id,
        current_version=secret.version_id,
        stages=secret.version_stages,
        is_rotation_ready=ready,
        summary=summary,
    )


def normalize_labels_text(labels: Mapping[str, Any], notes: str) -> str:
    label_parts = [f"{key}:{value}" for key, value in labels.items()]
    return " | ".join(label_parts + [notes])
