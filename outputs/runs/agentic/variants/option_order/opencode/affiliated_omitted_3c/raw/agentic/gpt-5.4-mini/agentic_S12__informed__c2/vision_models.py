from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _text(v: Any) -> str:
    if v is None:
        return ''
    if isinstance(v, bytes):
        return v.decode('utf-8', 'ignore')
    return str(v)


@dataclass
class ImageAnalysisRequest:
    image_path: str
    language: Optional[str] = None
    max_results: int = 10
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageLabel:
    name: str
    score: float = 0.0


@dataclass
class ImageTextBlock:
    text: str
    score: float = 0.0


@dataclass
class ImageSafetyFinding:
    category: str
    severity: str
    score: float = 0.0


@dataclass
class ImageAnalysisResult:
    labels: List[ImageLabel] = field(default_factory=list)
    description: str = ''
    text: List[ImageTextBlock] = field(default_factory=list)
    safety: List[ImageSafetyFinding] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_labels(items: Any) -> List[ImageLabel]:
    result = []
    for item in items or []:
        if isinstance(item, dict):
            result.append(ImageLabel(name=_text(item.get('name') or item.get('description') or item.get('entity')), score=float(item.get('score') or item.get('confidence') or 0.0)))
        else:
            result.append(ImageLabel(name=_text(item), score=0.0))
    return result


def normalize_text(items: Any) -> List[ImageTextBlock]:
    result = []
    for item in items or []:
        if isinstance(item, dict):
            result.append(ImageTextBlock(text=_text(item.get('text') or item.get('description') or item.get('value')), score=float(item.get('score') or item.get('confidence') or 0.0)))
        else:
            result.append(ImageTextBlock(text=_text(item), score=0.0))
    return result


def normalize_safety(items: Any) -> List[ImageSafetyFinding]:
    result = []
    for item in items or []:
        if isinstance(item, dict):
            result.append(ImageSafetyFinding(category=_text(item.get('category') or item.get('name') or item.get('label')), severity=_text(item.get('severity') or item.get('level') or 'unknown'), score=float(item.get('score') or item.get('confidence') or 0.0)))
        else:
            result.append(ImageSafetyFinding(category=_text(item), severity='unknown', score=0.0))
    return result
