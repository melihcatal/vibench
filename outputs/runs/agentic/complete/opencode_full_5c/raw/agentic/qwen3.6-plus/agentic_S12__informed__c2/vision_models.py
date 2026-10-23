from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ImageLabel:
    name: str
    confidence: float


@dataclass
class ImageObject:
    name: str
    confidence: float
    bounding_box: Optional[dict] = None


@dataclass
class DetectedTextRegion:
    text: str
    confidence: float
    bounding_box: Optional[dict] = None


@dataclass
class ImageDescription:
    caption: str
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class SafetyAssessment:
    is_safe: bool
    categories: dict = field(default_factory=dict)
    confidence: float = 0.0
    details: Optional[str] = None


@dataclass
class VisualAnalysisResult:
    labels: List[ImageLabel] = field(default_factory=list)
    objects: List[ImageObject] = field(default_factory=list)
    description: Optional[ImageDescription] = None
    detected_text: List[DetectedTextRegion] = field(default_factory=list)
    safety: Optional[SafetyAssessment] = None


def normalize_labels(raw_tags: list) -> List[ImageLabel]:
    labels = []
    for tag in raw_tags:
        name = tag.get("name", "")
        confidence = tag.get("confidence", 0.0)
        if name:
            labels.append(ImageLabel(name=name, confidence=confidence))
    return sorted(labels, key=lambda x: x.confidence, reverse=True)


def normalize_objects(raw_objects: list) -> List[ImageObject]:
    objects = []
    for obj in raw_objects:
        name = obj.get("name", "")
        confidence = obj.get("confidence", 0.0)
        bbox = obj.get("bounding_box")
        if name:
            objects.append(
                ImageObject(name=name, confidence=confidence, bounding_box=bbox)
            )
    return sorted(objects, key=lambda x: x.confidence, reverse=True)


def normalize_description(raw_caption: dict) -> ImageDescription:
    caption_text = raw_caption.get("text", "")
    confidence = raw_caption.get("confidence", 0.0)
    tags = raw_caption.get("tags", [])
    return ImageDescription(
        caption=caption_text,
        tags=tags,
        confidence=confidence,
    )


def normalize_detected_text(raw_read_result: dict) -> List[DetectedTextRegion]:
    regions = []
    for line in raw_read_result.get("lines", []):
        text = line.get("text", "")
        confidence = line.get("confidence", 0.0)
        bbox = line.get("bounding_box")
        if text:
            regions.append(
                DetectedTextRegion(text=text, confidence=confidence, bounding_box=bbox)
            )
    return regions


def normalize_safety(raw_safety: dict) -> SafetyAssessment:
    categories = raw_safety.get("categories", {})
    is_safe = raw_safety.get("is_safe", True)
    confidence = raw_safety.get("confidence", 0.0)
    details = raw_safety.get("details")
    return SafetyAssessment(
        is_safe=is_safe,
        categories=categories,
        confidence=confidence,
        details=details,
    )


def result_to_dict(result: VisualAnalysisResult) -> dict:
    return {
        "labels": [{"name": l.name, "confidence": l.confidence} for l in result.labels],
        "objects": [
            {
                "name": o.name,
                "confidence": o.confidence,
                "bounding_box": o.bounding_box,
            }
            for o in result.objects
        ],
        "description": {
            "caption": result.description.caption if result.description else "",
            "tags": result.description.tags if result.description else [],
            "confidence": result.description.confidence if result.description else 0.0,
        }
        if result.description
        else None,
        "detected_text": [
            {"text": t.text, "confidence": t.confidence, "bounding_box": t.bounding_box}
            for t in result.detected_text
        ],
        "safety": {
            "is_safe": result.safety.is_safe if result.safety else True,
            "categories": result.safety.categories if result.safety else {},
            "confidence": result.safety.confidence if result.safety else 0.0,
            "details": result.safety.details if result.safety else None,
        }
        if result.safety
        else None,
    }
