from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageSource:
    image_path: Optional[str] = None
    image_url: Optional[str] = None

    def require_value(self) -> str:
        if self.image_path:
            return self.image_path
        if self.image_url:
            return self.image_url
        raise ValueError("Either image_path or image_url must be provided")


@dataclass
class LabelDetectionResult:
    labels: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "google-cloud-vision"
    raw_response: Optional[Dict[str, Any]] = None

    def top_names(self, limit: int = 10) -> List[str]:
        return [item.get("name", "") for item in self.labels[:limit] if item.get("name")]


@dataclass
class ImageDescriptionResult:
    description: str
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TextDetectionResult:
    text: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "google-cloud-vision"
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyScoreResult:
    categories: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "google-cloud-vision"
    raw_response: Optional[Dict[str, Any]] = None

    def flagged_categories(self) -> List[str]:
        return [item["name"] for item in self.categories if item.get("flagged")]


@dataclass
class SummaryResult:
    summary: str
    provider: str = "anthropic"
    model: str = "claude-3-5-sonnet-20241022"
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str
    provider: str = "deepl"
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TextSafetyResult:
    flagged: bool
    categories: List[str] = field(default_factory=list)
    provider: str = "openai"
    model: str = "omni-moderation-latest"
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ArchiveResult:
    bucket: str
    object_name: str
    uri: str
    provider: str = "google-cloud-storage"


LIKELIHOOD_ORDER = {
    "UNKNOWN": 0,
    "VERY_UNLIKELY": 1,
    "UNLIKELY": 2,
    "POSSIBLE": 3,
    "LIKELY": 4,
    "VERY_LIKELY": 5,
}


def normalize_label_annotations(items: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items or []:
        normalized.append(
            {
                "name": getattr(item, "description", None),
                "score": float(getattr(item, "score", 0.0)),
                "mid": getattr(item, "mid", None),
            }
        )
    return normalized


def normalize_text_annotations(response: Any) -> TextDetectionResult:
    full_text = getattr(response, "full_text_annotation", None)
    text = getattr(full_text, "text", "") if full_text else ""
    blocks: List[Dict[str, Any]] = []
    for page in getattr(full_text, "pages", []) or []:
        for block in getattr(page, "blocks", []) or []:
            block_text_parts: List[str] = []
            for paragraph in getattr(block, "paragraphs", []) or []:
                for word in getattr(paragraph, "words", []) or []:
                    chars = [getattr(symbol, "text", "") for symbol in getattr(word, "symbols", []) or []]
                    block_text_parts.append("".join(chars))
            blocks.append({"text": " ".join(part for part in block_text_parts if part).strip()})
    return TextDetectionResult(text=text.strip(), blocks=blocks, raw_response=getattr(response, "_pb", None))


def normalize_safe_search(annotation: Any, threshold: str = "LIKELY") -> List[Dict[str, Any]]:
    threshold_value = LIKELIHOOD_ORDER[threshold]
    categories = {
        "adult": getattr(annotation, "adult", "UNKNOWN"),
        "spoof": getattr(annotation, "spoof", "UNKNOWN"),
        "medical": getattr(annotation, "medical", "UNKNOWN"),
        "violence": getattr(annotation, "violence", "UNKNOWN"),
        "racy": getattr(annotation, "racy", "UNKNOWN"),
    }
    normalized: List[Dict[str, Any]] = []
    for name, value in categories.items():
        likelihood = str(value)
        normalized.append(
            {
                "name": name,
                "likelihood": likelihood,
                "flagged": LIKELIHOOD_ORDER.get(likelihood, 0) >= threshold_value,
            }
        )
    return normalized
