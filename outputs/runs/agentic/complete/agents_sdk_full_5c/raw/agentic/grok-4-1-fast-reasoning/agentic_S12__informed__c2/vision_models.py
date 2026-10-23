from typing import TypedDict, List, Dict, Any

class Label(TypedDict):
    name: str
    confidence: float

class VisionLabels(TypedDict):
    labels: List[Label]

class Caption(TypedDict):
    text: str
    confidence: float

class VisionCaption(TypedDict):
    caption: Caption

class TextDet(TypedDict):
    text: str
    confidence: float

class VisionText(TypedDict):
    detections: List[TextDet]

class ModerationLabel(TypedDict):
    name: str
    confidence: float
    parent_name: str | None

class VisionSafety(TypedDict):
    moderation_labels: List[ModerationLabel]
    is_unsafe: bool

VisionResult = Dict[str, Any]