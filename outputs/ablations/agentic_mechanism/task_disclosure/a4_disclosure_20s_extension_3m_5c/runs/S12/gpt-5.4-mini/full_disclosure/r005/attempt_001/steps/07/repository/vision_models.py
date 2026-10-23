from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    prompt: str
    mime_type: Optional[str] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


@dataclass
class LabelItem:
    name: str
    confidence: Optional[float] = None
    score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageSummaryResult:
    text: str
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TextDetectionResult:
    text: str
    items: List[str] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class SafetyResult:
    unsafe: bool
    categories: List[str] = field(default_factory=list)
    score: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    return str(value).strip()


def normalize_label_item(value: Any) -> LabelItem:
    if isinstance(value, LabelItem):
        return value
    if isinstance(value, str):
        return LabelItem(name=value.strip())
    if not isinstance(value, dict):
        return LabelItem(name=normalize_text(value))
    metadata = dict(value)
    name = normalize_text(metadata.pop("name", metadata.pop("label", metadata.pop("text", ""))))
    confidence = metadata.pop("confidence", metadata.pop("score", None))
    return LabelItem(name=name, confidence=confidence, score=confidence, metadata=metadata)


def normalize_labels(value: Any) -> List[LabelItem]:
    if value is None:
        return []
    if isinstance(value, list):
        return [normalize_label_item(item) for item in value]
    return [normalize_label_item(value)]


def normalize_summary_response(value: Any) -> ImageSummaryResult:
    if isinstance(value, ImageSummaryResult):
        return value
    if isinstance(value, dict):
        text = normalize_text(value.get("text", value.get("summary", value.get("content", ""))))
        return ImageSummaryResult(text=text, raw=value)
    return ImageSummaryResult(text=normalize_text(value))


def normalize_text_detection_response(value: Any) -> TextDetectionResult:
    if isinstance(value, TextDetectionResult):
        return value
    if isinstance(value, dict):
        text = normalize_text(value.get("text", value.get("content", value.get("transcript", ""))))
        items = value.get("items", value.get("texts", []))
        if not isinstance(items, list):
            items = [items]
        return TextDetectionResult(text=text, items=[normalize_text(item) for item in items if normalize_text(item)], raw=value)
    text = normalize_text(value)
    return TextDetectionResult(text=text, items=[text] if text else [])


def normalize_safety_response(value: Any) -> SafetyResult:
    if isinstance(value, SafetyResult):
        return value
    if isinstance(value, dict):
        unsafe = bool(value.get("unsafe", value.get("flagged", False)))
        categories = value.get("categories", value.get("labels", []))
        if not isinstance(categories, list):
            categories = [categories]
        score = value.get("score", value.get("confidence"))
        return SafetyResult(unsafe=unsafe, categories=[normalize_text(category) for category in categories if normalize_text(category)], score=score, raw=value)
    return SafetyResult(unsafe=bool(value), raw={"value": value})
