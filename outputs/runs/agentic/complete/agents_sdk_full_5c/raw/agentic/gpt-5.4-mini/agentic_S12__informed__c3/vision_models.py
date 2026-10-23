from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    language: str = "en"
    max_results: int = 10


@dataclass
class LabelResult:
    name: str
    score: float


@dataclass
class TextDetectionResult:
    text: str
    confidence: float = 0.0


@dataclass
class SafetyResult:
    unsafe: bool
    categories: Dict[str, float]
    raw: Optional[Dict[str, Any]] = None


@dataclass
class DescriptionResult:
    description: str
    confidence: float = 0.0


@dataclass
class ArchiveRecord:
    bucket: str
    key: str
    uri: str


def normalize_labels(labels: Iterable[Any]) -> List[LabelResult]:
    normalized: List[LabelResult] = []
    for label in labels:
        name = getattr(label, "name", None) or getattr(label, "description", None) or str(label)
        score = float(getattr(label, "score", 0.0) or getattr(label, "confidence", 0.0) or 0.0)
        normalized.append(LabelResult(name=name, score=score))
    return normalized


def normalize_text(text_value: Any) -> TextDetectionResult:
    text = getattr(text_value, "text", None) or getattr(text_value, "description", None) or str(text_value)
    confidence = float(getattr(text_value, "confidence", 0.0) or getattr(text_value, "score", 0.0) or 0.0)
    return TextDetectionResult(text=text, confidence=confidence)


def extract_uri(record: Dict[str, Any], default_bucket: str, default_key: str) -> ArchiveRecord:
    bucket = record.get("bucket", default_bucket)
    key = record.get("key", default_key)
    uri = record.get("uri") or f"s3://{bucket}/{key}"
    return ArchiveRecord(bucket=bucket, key=key, uri=uri)
