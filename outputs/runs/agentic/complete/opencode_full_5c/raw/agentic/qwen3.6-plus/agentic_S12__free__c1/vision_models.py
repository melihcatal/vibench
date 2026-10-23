from __future__ import annotations

import base64
import io
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ImageSource(str, Enum):
    FILE_PATH = "file_path"
    URL = "url"
    BASE64 = "base64"


@dataclass
class ImageInput:
    source: ImageSource
    value: str
    mime_type: str = "image/jpeg"


@dataclass
class LabelItem:
    name: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None


@dataclass
class LabelResponse:
    labels: List[LabelItem]
    image_id: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DescriptionResponse:
    description: str
    confidence: float
    image_id: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextRegion:
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None
    language: str = "en"


@dataclass
class TextDetectionResponse:
    regions: List[TextRegion]
    full_text: str = ""
    image_id: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)


class SafetyCategory(str, Enum):
    VIOLENCE = "violence"
    ADULT = "adult"
    HATE = "hate"
    SELF_HARM = "self_harm"
    ILLEGAL = "illegal"
    MEDICAL = "medical"


@dataclass
class SafetyScore:
    category: SafetyCategory
    score: float
    flagged: bool


@dataclass
class SafetyResponse:
    scores: List[SafetyScore]
    overall_safe: bool
    image_id: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)


def encode_image_to_base64(image_path: str) -> tuple[str, str]:
    path = Path(image_path)
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime_type = mime_map.get(path.suffix.lower(), "image/jpeg")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return encoded, mime_type


def build_image_url_input(
    image_path: Optional[str] = None, image_url: Optional[str] = None
) -> ImageInput:
    if image_path:
        encoded, mime = encode_image_to_base64(image_path)
        return ImageInput(source=ImageSource.BASE64, value=encoded, mime_type=mime)
    if image_url:
        return ImageInput(source=ImageSource.URL, value=image_url)
    raise ValueError("Either image_path or image_url must be provided")


def normalize_label_confidence(raw_score: float) -> float:
    return max(0.0, min(1.0, float(raw_score)))


def normalize_safety_score(raw_score: float) -> float:
    return max(0.0, min(1.0, float(raw_score)))


def extract_text_from_regions(regions: List[TextRegion]) -> str:
    return " ".join(r.text for r in regions if r.text.strip())


def label_response_to_dict(response: LabelResponse) -> Dict[str, Any]:
    return {
        "image_id": response.image_id,
        "labels": [
            {"name": l.name, "confidence": l.confidence, "bounding_box": l.bounding_box}
            for l in response.labels
        ],
    }


def description_response_to_dict(response: DescriptionResponse) -> Dict[str, Any]:
    return {
        "image_id": response.image_id,
        "description": response.description,
        "confidence": response.confidence,
    }


def text_detection_response_to_dict(response: TextDetectionResponse) -> Dict[str, Any]:
    return {
        "image_id": response.image_id,
        "full_text": response.full_text,
        "regions": [
            {
                "text": r.text,
                "confidence": r.confidence,
                "language": r.language,
                "bounding_box": r.bounding_box,
            }
            for r in response.regions
        ],
    }


def safety_response_to_dict(response: SafetyResponse) -> Dict[str, Any]:
    return {
        "image_id": response.image_id,
        "overall_safe": response.overall_safe,
        "scores": [
            {"category": s.category.value, "score": s.score, "flagged": s.flagged}
            for s in response.scores
        ],
    }
