from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageSource:
    path: Optional[str] = None
    uri: Optional[str] = None
    mime_type: Optional[str] = None


@dataclass
class LabelDetection:
    name: str
    confidence: float
    categories: List[str] = field(default_factory=list)


@dataclass
class OCRTextBlock:
    text: str
    confidence: float
    block_type: str = "text"


@dataclass
class SafetyCategory:
    name: str
    likelihood: str
    score: Optional[float] = None


@dataclass
class VisualDescription:
    text: str
    model: str
    provider: str


@dataclass
class AnalysisSummary:
    labels: List[str] = field(default_factory=list)
    description: Optional[str] = None
    ocr_text: List[str] = field(default_factory=list)
    safety_flags: List[str] = field(default_factory=list)


@dataclass
class ArchiveArtifact:
    key: str
    etag: Optional[str] = None
    uri: Optional[str] = None


def top_label_names(items: Iterable[Dict[str, Any]], limit: int = 10) -> List[str]:
    sorted_items = sorted(items, key=lambda x: float(x.get("confidence", 0.0)), reverse=True)
    return [str(item.get("name", "")).strip() for item in sorted_items[:limit] if item.get("name")]


def normalize_vision_labels(raw_labels: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in raw_labels:
        categories = item.get("categories") or []
        normalized.append(
            {
                "name": str(item.get("name", "")).strip(),
                "confidence": round(float(item.get("confidence", 0.0)), 4),
                "categories": [str(category).strip() for category in categories if category],
            }
        )
    return normalized


def normalize_ocr_blocks(raw_blocks: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for block in raw_blocks:
        normalized.append(
            {
                "text": str(block.get("text", "")).strip(),
                "confidence": round(float(block.get("confidence", 0.0)), 4),
                "block_type": str(block.get("block_type", "text")),
            }
        )
    return [item for item in normalized if item["text"]]


def normalize_safety_categories(raw_categories: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for name, value in raw_categories.items():
        if isinstance(value, dict):
            likelihood = str(value.get("likelihood", "unknown"))
            score = value.get("score")
        else:
            likelihood = str(value)
            score = None
        normalized.append({"name": str(name), "likelihood": likelihood, "score": score})
    return normalized


def compact_text_list(values: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for value in values:
        item = str(value).strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result
