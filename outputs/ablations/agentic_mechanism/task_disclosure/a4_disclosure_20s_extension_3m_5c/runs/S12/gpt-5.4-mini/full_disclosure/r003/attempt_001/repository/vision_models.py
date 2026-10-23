from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return default


def _coerce_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _coerce_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass(slots=True)
class VisionImageRequest:
    image: str
    prompt: str = ""
    language: str = "en"
    max_results: int = 5
    sensitivity: str = "standard"
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "VisionImageRequest":
        return cls(
            image=_coerce_str(data.get("image")),
            prompt=_coerce_str(data.get("prompt")),
            language=_coerce_str(data.get("language")) or "en",
            max_results=int(_coerce_float(data.get("max_results"), 5)),
            sensitivity=_coerce_str(data.get("sensitivity")) or "standard",
            metadata=_coerce_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class VisionTextRequest:
    image: str
    include_confidence: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "VisionTextRequest":
        return cls(
            image=_coerce_str(data.get("image")),
            include_confidence=_coerce_bool(data.get("include_confidence")),
            metadata=_coerce_mapping(data.get("metadata")),
        )


@dataclass(slots=True)
class VisionLabel:
    name: str
    confidence: float = 0.0
    score: float = 0.0
    category: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "VisionLabel":
        return cls(
            name=_coerce_str(data.get("name") or data.get("label")),
            confidence=_coerce_float(data.get("confidence")),
            score=_coerce_float(data.get("score"), _coerce_float(data.get("confidence"))),
            category=_coerce_str(data.get("category")),
        )


@dataclass(slots=True)
class VisionTextBlock:
    text: str
    confidence: float = 0.0
    language: str = ""
    bbox: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "VisionTextBlock":
        return cls(
            text=_coerce_str(data.get("text")),
            confidence=_coerce_float(data.get("confidence")),
            language=_coerce_str(data.get("language")),
            bbox=_coerce_mapping(data.get("bbox") or data.get("bounding_box")),
        )


@dataclass(slots=True)
class VisionSafetyFinding:
    category: str
    severity: str = ""
    confidence: float = 0.0
    flagged: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "VisionSafetyFinding":
        return cls(
            category=_coerce_str(data.get("category") or data.get("name")),
            severity=_coerce_str(data.get("severity")),
            confidence=_coerce_float(data.get("confidence")),
            flagged=_coerce_bool(data.get("flagged") or data.get("unsafe")),
        )


@dataclass(slots=True)
class VisionAnalysisResult:
    summary: str = ""
    labels: list[VisionLabel] = field(default_factory=list)
    text_blocks: list[VisionTextBlock] = field(default_factory=list)
    safety_findings: list[VisionSafetyFinding] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "VisionAnalysisResult":
        labels = [VisionLabel.from_mapping(item) for item in _coerce_list(data.get("labels")) if isinstance(item, Mapping)]
        text_blocks = [VisionTextBlock.from_mapping(item) for item in _coerce_list(data.get("text_blocks") or data.get("text")) if isinstance(item, Mapping)]
        safety_findings = [VisionSafetyFinding.from_mapping(item) for item in _coerce_list(data.get("safety_findings") or data.get("safety")) if isinstance(item, Mapping)]
        return cls(
            summary=_coerce_str(data.get("summary") or data.get("description")),
            labels=labels,
            text_blocks=text_blocks,
            safety_findings=safety_findings,
            raw=dict(data),
        )


def normalize_labels(value: Any) -> list[VisionLabel]:
    items = _coerce_list(value)
    return [VisionLabel.from_mapping(item) for item in items if isinstance(item, Mapping)]


def normalize_text_blocks(value: Any) -> list[VisionTextBlock]:
    items = _coerce_list(value)
    return [VisionTextBlock.from_mapping(item) for item in items if isinstance(item, Mapping)]


def normalize_safety_findings(value: Any) -> list[VisionSafetyFinding]:
    items = _coerce_list(value)
    return [VisionSafetyFinding.from_mapping(item) for item in items if isinstance(item, Mapping)]


def normalize_analysis_result(value: Any) -> VisionAnalysisResult:
    if isinstance(value, VisionAnalysisResult):
        return value
    if isinstance(value, Mapping):
        return VisionAnalysisResult.from_mapping(value)
    return VisionAnalysisResult(raw={"value": value})


def build_description(summary: str, labels: Sequence[VisionLabel] | None = None, text_blocks: Sequence[VisionTextBlock] | None = None) -> str:
    parts: list[str] = []
    summary = _coerce_str(summary).strip()
    if summary:
        parts.append(summary)
    if labels:
        names = [label.name for label in labels if label.name]
        if names:
            parts.append("Labels: " + ", ".join(names))
    if text_blocks:
        texts = [block.text for block in text_blocks if block.text]
        if texts:
            parts.append("Text: " + " | ".join(texts))
    return " ".join(parts).strip()
