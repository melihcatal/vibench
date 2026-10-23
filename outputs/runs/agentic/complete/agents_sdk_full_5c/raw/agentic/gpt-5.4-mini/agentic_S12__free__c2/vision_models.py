from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class LabelDetectionResult:
    labels: List[Dict[str, Any]]
    raw_response: Any


@dataclass
class DescriptionResult:
    description: str
    raw_response: Any


@dataclass
class TextDetectionResult:
    text_blocks: List[Dict[str, Any]]
    raw_response: Any


@dataclass
class SafetyScoreResult:
    score: Dict[str, Any]
    raw_response: Any


def normalize_labels(label_annotations: Any) -> List[Dict[str, Any]]:
    return [
        {"description": getattr(label, "description", ""), "score": float(getattr(label, "score", 0.0))}
        for label in (label_annotations or [])
    ]


def normalize_description(text: str) -> str:
    return (text or "").strip()


def normalize_text_blocks(text_annotations: Any) -> List[Dict[str, Any]]:
    return [
        {"text": getattr(block, "description", ""), "locale": getattr(block, "locale", "")}
        for block in (text_annotations or [])
    ]


def score_safe_search(safe_search_annotation: Any) -> Dict[str, Any]:
    if safe_search_annotation is None:
        return {}
    return {
        "adult": getattr(safe_search_annotation, "adult", None),
        "spoof": getattr(safe_search_annotation, "spoof", None),
        "medical": getattr(safe_search_annotation, "medical", None),
        "violence": getattr(safe_search_annotation, "violence", None),
        "racy": getattr(safe_search_annotation, "racy", None),
    }
