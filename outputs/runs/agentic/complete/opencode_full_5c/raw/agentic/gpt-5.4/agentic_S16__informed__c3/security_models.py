from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class SecretReference:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretPayload:
    name: str
    value: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    parsed_json: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RotationSummary:
    secret_id: str
    current_version: Optional[str]
    previous_version: Optional[str]
    stages: Dict[str, List[str]]
    last_rotated_date: Optional[str]


@dataclass
class LabelSafetyReport:
    text: str
    unsafe: bool
    risk_scores: Dict[str, float]
    flagged_categories: List[str]


@dataclass
class AuditEmbedding:
    text: str
    vector: List[float]
    model: str
    dimensions: int


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None


def normalize_secret_payload(payload: SecretPayload) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "name": payload.name,
        "value": payload.value,
        "version_id": payload.version_id,
        "version_stage": payload.version_stage,
        "metadata": dict(payload.metadata),
    }
    if payload.parsed_json is not None:
        result["parsed_json"] = payload.parsed_json
    return result


def normalize_rotation_summary(summary: RotationSummary) -> Dict[str, Any]:
    return {
        "secret_id": summary.secret_id,
        "current_version": summary.current_version,
        "previous_version": summary.previous_version,
        "stages": summary.stages,
        "last_rotated_date": summary.last_rotated_date,
    }


def normalize_label_safety(report: LabelSafetyReport) -> Dict[str, Any]:
    return {
        "text": report.text,
        "unsafe": report.unsafe,
        "risk_scores": report.risk_scores,
        "flagged_categories": report.flagged_categories,
    }


def normalize_embedding(embedding: AuditEmbedding) -> Dict[str, Any]:
    return {
        "text": embedding.text,
        "vector": embedding.vector,
        "model": embedding.model,
        "dimensions": embedding.dimensions,
    }


def normalize_translation(result: TranslationResult) -> Dict[str, Any]:
    return {
        "source_text": result.source_text,
        "translated_text": result.translated_text,
        "target_language": result.target_language,
        "detected_source_language": result.detected_source_language,
    }


def coerce_string_map(value: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(k): str(v) for k, v in value.items()}
