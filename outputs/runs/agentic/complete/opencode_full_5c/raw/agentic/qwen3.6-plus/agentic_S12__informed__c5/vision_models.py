import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ImageSource:
    url: Optional[str] = None
    bytes_data: Optional[bytes] = None
    content_type: Optional[str] = None


@dataclass
class BoundingBox:
    left: float = 0.0
    top: float = 0.0
    width: float = 0.0
    height: float = 0.0


@dataclass
class DetectedLabel:
    name: str
    confidence: float
    parents: List[str] = field(default_factory=list)


@dataclass
class DetectedText:
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    type_: str = "WORD"


@dataclass
class ModerationLabel:
    name: str
    confidence: float
    parent_name: Optional[str] = None


@dataclass
class LabelDetectionResponse:
    image_url: Optional[str] = None
    labels: List[DetectedLabel] = field(default_factory=list)
    label_model_version: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ImageDescriptionResponse:
    image_url: Optional[str] = None
    description: str = ""
    confidence: float = 0.0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TextDetectionResponse:
    image_url: Optional[str] = None
    detected_text: List[DetectedText] = field(default_factory=list)
    full_text: str = ""
    text_model_version: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyScoreResponse:
    image_url: Optional[str] = None
    moderation_labels: List[ModerationLabel] = field(default_factory=list)
    is_safe: bool = True
    highest_confidence_label: Optional[str] = None
    moderation_model_version: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


def normalize_image_source(
    image_url: Optional[str] = None, image_bytes: Optional[bytes] = None
) -> ImageSource:
    source = ImageSource()
    if image_bytes:
        source.bytes_data = image_bytes
        if image_url:
            source.url = image_url
    elif image_url:
        source.url = image_url
    return source


def build_rekognition_image_arg(image_source: ImageSource) -> Dict[str, Any]:
    if image_source.bytes_data:
        return {"Bytes": image_source.bytes_data}
    if image_source.url:
        return {"S3Object": {"Bucket": "", "Name": ""}}
    return {}


def parse_rekognition_labels(
    raw: Dict[str, Any], image_url: Optional[str] = None
) -> LabelDetectionResponse:
    labels = []
    for item in raw.get("Labels", []):
        parents = [p["Name"] for p in item.get("Parents", [])]
        labels.append(
            DetectedLabel(
                name=item["Name"], confidence=item["Confidence"], parents=parents
            )
        )
    return LabelDetectionResponse(
        image_url=image_url,
        labels=labels,
        label_model_version=raw.get("LabelModelVersion"),
        raw_response=raw,
    )


def parse_rekognition_text(
    raw: Dict[str, Any], image_url: Optional[str] = None
) -> TextDetectionResponse:
    detected_texts = []
    full_text_parts = []
    for item in raw.get("TextDetections", []):
        if item["Type"] == "LINE":
            full_text_parts.append(item["DetectedText"])
        bb_data = item.get("Geometry", {}).get("BoundingBox", {})
        bounding_box = (
            BoundingBox(
                left=bb_data.get("Left", 0.0),
                top=bb_data.get("Top", 0.0),
                width=bb_data.get("Width", 0.0),
                height=bb_data.get("Height", 0.0),
            )
            if bb_data
            else None
        )
        detected_texts.append(
            DetectedText(
                text=item.get("DetectedText", ""),
                confidence=item["Confidence"],
                bounding_box=bounding_box,
                type_=item["Type"],
            )
        )
    return TextDetectionResponse(
        image_url=image_url,
        detected_text=detected_texts,
        full_text=" ".join(full_text_parts),
        text_model_version=raw.get("TextModelVersion"),
        raw_response=raw,
    )


def parse_rekognition_moderation(
    raw: Dict[str, Any], image_url: Optional[str] = None, threshold: float = 50.0
) -> SafetyScoreResponse:
    labels = []
    highest_conf = 0.0
    highest_name = None
    for item in raw.get("ModerationLabels", []):
        conf = item["Confidence"]
        labels.append(
            ModerationLabel(
                name=item["Name"], confidence=conf, parent_name=item.get("ParentName")
            )
        )
        if conf > highest_conf:
            highest_conf = conf
            highest_name = item["Name"]
    is_safe = highest_conf < threshold
    return SafetyScoreResponse(
        image_url=image_url,
        moderation_labels=labels,
        is_safe=is_safe,
        highest_confidence_label=highest_name,
        moderation_model_version=raw.get("ModerationModelVersion"),
        raw_response=raw,
    )
