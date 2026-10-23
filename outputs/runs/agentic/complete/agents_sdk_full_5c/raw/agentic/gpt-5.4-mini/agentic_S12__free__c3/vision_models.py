from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass
class LabelDetectionResult:
    labels: List[Dict[str, Any]]
    raw: Any


@dataclass
class ImageDescriptionResult:
    description: str
    raw: Any


@dataclass
class OCRResult:
    text: str
    words: List[str]
    raw: Any


@dataclass
class SafetyScoreResult:
    score: Dict[str, Any]
    raw: Any


def normalize_label_items(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        name = item.get("name") or item.get("description")
        confidence = item.get("confidence")
        if name:
            normalized.append({"name": str(name), "confidence": confidence})
    return normalized


def normalize_text_items(items: Iterable[str]) -> List[str]:
    return [str(item).strip() for item in items if str(item).strip()]


def normalize_safety_score(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "violence": data.get("violence", data.get("categories", {}).get("violence")),
        "self_harm": data.get("self_harm", data.get("categories", {}).get("self_harm")),
        "nudity": data.get("nudity", data.get("categories", {}).get("nudity")),
        "raw": data,
    }
