from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


@dataclass(frozen=True)
class ImageAnalysisRequest:
    image_url: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: Optional[str] = None
    features: Sequence[str] = field(default_factory=tuple)
    prompt: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "image_url": _normalize_text(self.image_url) or None,
            "mime_type": _normalize_text(self.mime_type) or None,
            "features": [str(feature).strip() for feature in self.features if str(feature).strip()],
            "prompt": _normalize_text(self.prompt) or None,
            "metadata": dict(self.metadata),
        }
        if self.image_bytes is not None:
            payload["image_bytes"] = self.image_bytes
        return {key: value for key, value in payload.items() if value not in (None, [], {})}


@dataclass(frozen=True)
class BoundingBox:
    left: float = 0.0
    top: float = 0.0
    width: float = 0.0
    height: float = 0.0

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "BoundingBox":
        return cls(
            left=_coerce_float(data.get("left") or data.get("x") or data.get("xmin")),
            top=_coerce_float(data.get("top") or data.get("y") or data.get("ymin")),
            width=_coerce_float(data.get("width") or data.get("w") or data.get("xmax")),
            height=_coerce_float(data.get("height") or data.get("h") or data.get("ymax")),
        )

    def to_dict(self) -> Dict[str, float]:
        return {"left": self.left, "top": self.top, "width": self.width, "height": self.height}


@dataclass(frozen=True)
class Label:
    name: str
    score: float = 0.0
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Label":
        bbox = data.get("bounding_box") or data.get("boundingBox") or data.get("box")
        return cls(
            name=_normalize_text(data.get("name") or data.get("label") or data.get("text")),
            score=_coerce_float(data.get("score") or data.get("confidence")),
            confidence=_coerce_float(data.get("confidence") or data.get("score")),
            bounding_box=BoundingBox.from_mapping(bbox) if isinstance(bbox, Mapping) else None,
            metadata={k: v for k, v in dict(data).items() if k not in {"name", "label", "text", "score", "confidence", "bounding_box", "boundingBox", "box"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"name": self.name, "score": self.score, "confidence": self.confidence, "metadata": dict(self.metadata)}
        if self.bounding_box is not None:
            result["bounding_box"] = self.bounding_box.to_dict()
        return result


@dataclass(frozen=True)
class SafetyResult:
    safe: bool = True
    score: float = 0.0
    categories: Sequence[str] = field(default_factory=tuple)
    details: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SafetyResult":
        categories = _normalize_list(data.get("categories") or data.get("labels") or data.get("flags"))
        return cls(
            safe=bool(data.get("safe", data.get("is_safe", True))),
            score=_coerce_float(data.get("score") or data.get("confidence")),
            categories=tuple(_normalize_text(item) for item in categories if _normalize_text(item)),
            details={k: v for k, v in dict(data).items() if k not in {"safe", "is_safe", "score", "confidence", "categories", "labels", "flags"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"safe": self.safe, "score": self.score, "categories": list(self.categories), "details": dict(self.details)}


@dataclass(frozen=True)
class TextDetectionResult:
    text: str = ""
    confidence: float = 0.0
    words: Sequence[str] = field(default_factory=tuple)
    details: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TextDetectionResult":
        words = _normalize_list(data.get("words") or data.get("tokens"))
        return cls(
            text=_normalize_text(data.get("text") or data.get("description")),
            confidence=_coerce_float(data.get("confidence") or data.get("score")),
            words=tuple(_normalize_text(word) for word in words if _normalize_text(word)),
            details={k: v for k, v in dict(data).items() if k not in {"text", "description", "confidence", "score", "words", "tokens"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence, "words": list(self.words), "details": dict(self.details)}


@dataclass(frozen=True)
class SummaryResult:
    summary: str = ""
    highlights: Sequence[str] = field(default_factory=tuple)
    details: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SummaryResult":
        highlights = _normalize_list(data.get("highlights") or data.get("bullets") or data.get("items"))
        return cls(
            summary=_normalize_text(data.get("summary") or data.get("text") or data.get("description")),
            highlights=tuple(_normalize_text(item) for item in highlights if _normalize_text(item)),
            details={k: v for k, v in dict(data).items() if k not in {"summary", "text", "description", "highlights", "bullets", "items"}},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "highlights": list(self.highlights), "details": dict(self.details)}


def normalize_labels(value: Iterable[Any]) -> List[Dict[str, Any]]:
    return [item.to_dict() if isinstance(item, Label) else Label.from_mapping(item).to_dict() if isinstance(item, Mapping) else {"name": _normalize_text(item)} for item in value]


def normalize_safety_result(value: Mapping[str, Any]) -> Dict[str, Any]:
    return SafetyResult.from_mapping(value).to_dict()


def normalize_text_result(value: Mapping[str, Any]) -> Dict[str, Any]:
    return TextDetectionResult.from_mapping(value).to_dict()


def normalize_summary_result(value: Mapping[str, Any]) -> Dict[str, Any]:
    return SummaryResult.from_mapping(value).to_dict()
