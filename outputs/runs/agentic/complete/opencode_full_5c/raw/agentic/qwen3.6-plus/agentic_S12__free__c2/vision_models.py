from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class BoundingBox:
    width: float = 0.0
    height: float = 0.0
    left: float = 0.0
    top: float = 0.0

    @classmethod
    def from_aws(cls, aws_bbox: Dict[str, float]) -> "BoundingBox":
        return cls(
            width=aws_bbox.get("Width", 0.0),
            height=aws_bbox.get("Height", 0.0),
            left=aws_bbox.get("Left", 0.0),
            top=aws_bbox.get("Top", 0.0),
        )


@dataclass
class ImageLabel:
    name: str
    confidence: float
    instances: List[Dict[str, Any]] = field(default_factory=list)
    parents: List[str] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None


@dataclass
class ImageLabelRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    max_labels: int = 10
    min_confidence: float = 50.0


@dataclass
class ImageLabelResponse:
    labels: List[ImageLabel]
    label_model: str = "aws-rekognition-detect-labels-v3"
    orientation_correction: Optional[str] = None


def normalize_label(
    name: str,
    confidence: float,
    instances: Optional[List[Dict[str, Any]]] = None,
    parents: Optional[List[str]] = None,
    bounding_box: Optional[Dict[str, float]] = None,
) -> ImageLabel:
    bbox = BoundingBox.from_aws(bounding_box) if bounding_box else None
    return ImageLabel(
        name=name,
        confidence=confidence,
        instances=instances or [],
        parents=parents or [],
        bounding_box=bbox,
    )


@dataclass
class ImageDescriptionRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    max_descriptions: int = 3
    min_confidence: float = 60.0


@dataclass
class ImageDescriptionResponse:
    descriptions: List[str]
    model: str = "aws-rekognition-describe-image-v3"
    primary_labels: List[str] = field(default_factory=list)


@dataclass
class DetectedTextBlock:
    detected_text: str
    text_type: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None
    parent_id: Optional[int] = None
    id: Optional[int] = None


@dataclass
class ImageTextRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    detect_orientation: bool = True


@dataclass
class ImageTextResponse:
    text_blocks: List[DetectedTextBlock]
    full_text: str
    lines: List[DetectedTextBlock] = field(default_factory=list)
    words: List[DetectedTextBlock] = field(default_factory=list)
    model: str = "aws-rekognition-detect-text-v3"


@dataclass
class SafetyModerationLabel:
    name: str
    parent_name: str
    confidence: float
    category: str


@dataclass
class ImageSafetyRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    custom_categories: Optional[List[str]] = None


@dataclass
class ImageSafetyResponse:
    is_safe: bool
    safety_score: float
    moderation_labels: List[SafetyModerationLabel]
    unsafe_detections: List[SafetyModerationLabel]
    model: str = "aws-rekognition-detect-moderation-labels-v3"


def normalize_safety_response(
    aws_response: Dict[str, Any],
    categories: Optional[List[str]] = None,
) -> ImageSafetyResponse:
    from score_image_safety import UNSAFE_CATEGORIES, SAFE_THRESHOLD

    cats = set(categories) if categories else UNSAFE_CATEGORIES

    moderation_labels = []
    unsafe_detections = []
    max_unsafe_confidence = 0.0

    for mod_label in aws_response.get("ModerationLabels", []):
        label_name = mod_label.get("Name", "")
        parent_name = mod_label.get("ParentName", "")
        confidence = mod_label.get("Confidence", 0.0)

        safety_label = SafetyModerationLabel(
            name=label_name,
            parent_name=parent_name,
            confidence=confidence,
            category=label_name,
        )
        moderation_labels.append(safety_label)

        if (label_name in cats or parent_name in cats) and confidence >= SAFE_THRESHOLD:
            unsafe_detections.append(safety_label)
            max_unsafe_confidence = max(max_unsafe_confidence, confidence)

    is_safe = len(unsafe_detections) == 0
    safety_score = max(0.0, 100.0 - max_unsafe_confidence) if not is_safe else 100.0

    return ImageSafetyResponse(
        is_safe=is_safe,
        safety_score=safety_score,
        moderation_labels=moderation_labels,
        unsafe_detections=unsafe_detections,
        model="aws-rekognition-detect-moderation-labels-v3",
    )
