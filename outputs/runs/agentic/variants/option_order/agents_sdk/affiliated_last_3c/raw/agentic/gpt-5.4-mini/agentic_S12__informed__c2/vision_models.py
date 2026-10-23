from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ImageRequest:
    image_path: str
    language: str = "en"
    max_results: int = 10


@dataclass
class LabelResult:
    name: str
    score: float


@dataclass
class TextResult:
    text: str
    score: float = 0.0


@dataclass
class SafetyResult:
    safe: bool
    categories: Dict[str, float]
    reason: str = ""


@dataclass
class DescriptionResult:
    text: str
    confidence: float = 0.0


@dataclass
class ArchiveArtifact:
    key: str
    uri: str
    metadata: Dict[str, Any]


def normalize_labels(items: Iterable[Mapping[str, Any]], limit: Optional[int] = None) -> List[LabelResult]:
    results: List[LabelResult] = []
    for item in items:
        name = str(item.get("name") or item.get("description") or item.get("label") or "")
        score = float(item.get("score") or item.get("confidence") or 0.0)
        if name:
            results.append(LabelResult(name=name, score=score))
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit] if limit is not None else results


def normalize_texts(items: Iterable[Mapping[str, Any]], limit: Optional[int] = None) -> List[TextResult]:
    results: List[TextResult] = []
    for item in items:
        text = str(item.get("text") or item.get("description") or "").strip()
        score = float(item.get("score") or item.get("confidence") or 0.0)
        if text:
            results.append(TextResult(text=text, score=score))
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit] if limit is not None else results


def safe_text_summary(text: str, max_len: int = 240) -> str:
    cleaned = " ".join(text.split())
    return cleaned[:max_len]
