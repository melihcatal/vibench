from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LabelResult:
    labels: List[Dict[str, Any]]


@dataclass
class TextResult:
    text_detections: List[Dict[str, Any]]


@dataclass
class SafetyResult:
    moderation_labels: List[Dict[str, Any]]


def normalize_labels(response: Dict[str, Any]) -> LabelResult:
    return LabelResult(labels=response.get("Labels", []))


def normalize_text(response: Dict[str, Any]) -> TextResult:
    return TextResult(text_detections=response.get("TextDetections", []))


def normalize_safety(response: Dict[str, Any]) -> SafetyResult:
    moderation = []
    for key in ("Labels", "ModerationLabels"):
        moderation.extend(response.get(key, []))
    return SafetyResult(moderation_labels=moderation)


def compact_text(items: List[Dict[str, Any]]) -> str:
    parts = []
    for item in items:
        text = item.get("DetectedText") or item.get("Name") or ""
        if text:
            parts.append(text)
    return " ".join(parts).strip()
