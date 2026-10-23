from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageInput:
    image_path: Optional[str] = None
    image_b64: Optional[str] = None

    def validate(self) -> None:
        if not self.image_path and not self.image_b64:
            raise ValueError("image_path or image_b64 is required")


@dataclass
class LabelItem:
    name: str
    confidence: float


@dataclass
class ObjectItem:
    name: str
    confidence: float
    box: Dict[str, float] = field(default_factory=dict)


@dataclass
class TextItem:
    text: str
    confidence: float = 0.0


@dataclass
class SafetyItem:
    category: str
    score: float
    flagged: bool


@dataclass
class ImageAnalysisResult:
    summary: str = ""
    labels: List[LabelItem] = field(default_factory=list)
    objects: List[ObjectItem] = field(default_factory=list)
    text: List[TextItem] = field(default_factory=list)
    safety: List[SafetyItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_labels(raw_result: Any) -> List[LabelItem]:
    items: List[LabelItem] = []
    for tag in getattr(raw_result, "tags", []) or []:
        items.append(LabelItem(name=getattr(tag, "name", ""), confidence=float(getattr(tag, "confidence", 0.0))))
    return items


def normalize_objects(raw_result: Any) -> List[ObjectItem]:
    items: List[ObjectItem] = []
    for obj in getattr(raw_result, "objects", []) or []:
        box = getattr(obj, "bounding_box", None)
        box_dict = {}
        if box is not None:
            box_dict = {
                "x": float(getattr(box, "x", 0.0)),
                "y": float(getattr(box, "y", 0.0)),
                "w": float(getattr(box, "w", 0.0)),
                "h": float(getattr(box, "h", 0.0)),
            }
        items.append(ObjectItem(name=getattr(obj, "name", ""), confidence=float(getattr(obj, "confidence", 0.0)), box=box_dict))
    return items


def normalize_text(raw_result: Any) -> List[TextItem]:
    items: List[TextItem] = []
    read = getattr(raw_result, "read", None)
    if read and getattr(read, "blocks", None):
        for block in read.blocks:
            for line in getattr(block, "lines", []) or []:
                items.append(TextItem(text=getattr(line, "text", ""), confidence=float(getattr(line, "confidence", 0.0))))
    return items


def normalize_caption(raw_result: Any) -> str:
    caption = getattr(raw_result, "caption", None)
    if caption is None:
        return ""
    return str(getattr(caption, "text", "") or "")


def normalize_safety_from_labels(raw_result: Any, threshold: float = 0.5) -> List[SafetyItem]:
    safety = []
    for tag in getattr(raw_result, "tags", []) or []:
        score = float(getattr(tag, "confidence", 0.0))
        safety.append(SafetyItem(category=getattr(tag, "name", ""), score=score, flagged=score >= threshold and getattr(tag, "name", "").lower() in {"adult", "racy", "gore", "violence", "weapon"}))
    return safety
