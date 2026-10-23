from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    uri: Optional[str] = None
    content: Optional[bytes] = None
    mime_type: str = "image/jpeg"


@dataclass
class LabelDetection:
    name: str
    score: float


@dataclass
class OCRTextBlock:
    text: str
    score: float


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
class ImageLabelsResult:
    provider: str
    labels: List[LabelDetection] = field(default_factory=list)


@dataclass
class ImageTextResult:
    provider: str
    text_blocks: List[OCRTextBlock] = field(default_factory=list)
    full_text: str = ""


@dataclass
class ImageSafetyResult:
    provider: str
    categories: List[SafetyCategory] = field(default_factory=list)
    is_sensitive: bool = False


def normalize_score(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return 0.0
    value = float(value)
    if value > 1.0:
        return round(value / 100.0, 6)
    return round(value, 6)


def dataclass_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)


def labels_result_dict(result: ImageLabelsResult) -> Dict[str, Any]:
    return dataclass_dict(result)


def text_result_dict(result: ImageTextResult) -> Dict[str, Any]:
    return dataclass_dict(result)


def safety_result_dict(result: ImageSafetyResult) -> Dict[str, Any]:
    return dataclass_dict(result)


def description_result_dict(result: VisualDescription) -> Dict[str, Any]:
    return dataclass_dict(result)
