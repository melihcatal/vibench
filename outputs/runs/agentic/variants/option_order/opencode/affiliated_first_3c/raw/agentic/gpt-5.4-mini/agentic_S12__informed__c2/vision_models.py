from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageInput:
    image_path: str
    image_url: Optional[str] = None


@dataclass
class LabelDetectionResult:
    labels: List[str]
    raw: Dict[str, Any]


@dataclass
class DescriptionResult:
    description: str
    raw: Dict[str, Any]


@dataclass
class TextDetectionResult:
    texts: List[str]
    raw: Dict[str, Any]


@dataclass
class SafetyResult:
    unsafe: bool
    categories: List[str]
    raw: Dict[str, Any]


def normalize_strings(values: Any) -> List[str]:
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    return [str(v) for v in values if str(v).strip()]
