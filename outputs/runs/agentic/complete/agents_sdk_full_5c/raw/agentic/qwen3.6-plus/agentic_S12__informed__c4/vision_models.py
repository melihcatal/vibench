"""
vision_models.py - Define local request, response, and normalization helpers
for Static Image and Visual Understanding tasks.

Provides Pydantic-style dataclasses and normalization utilities for
image analysis payloads across label detection, image description,
text detection, and safety scoring workflows.
"""

from __future__ import annotations

import base64
import io
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ImageSourceType(str, Enum):
    URL = "url"
    FILE = "file"
    BYTES = "bytes"


@dataclass
class ImageAnalysisRequest:
    """Normalized input request for vision analysis operations."""

    image_source: Optional[str] = None
    image_bytes: Optional[bytes] = None
    source_type: ImageSourceType = ImageSourceType.URL
    mime_type: Optional[str] = None
    max_results: int = 10
    language_hints: List[str] = field(default_factory=lambda: ["en"])

    @classmethod
    def from_url(cls, url: str, **kwargs: Any) -> "ImageAnalysisRequest":
        return cls(image_source=url, source_type=ImageSourceType.URL, **kwargs)

    @classmethod
    def from_file(cls, filepath: str, **kwargs: Any) -> "ImageAnalysisRequest":
        with open(filepath, "rb") as fh:
            data = fh.read()
        mime = kwargs.pop("mime_type", None) or _guess_mime(filepath)
        return cls(image_bytes=data, source_type=ImageSourceType.FILE, mime_type=mime, **kwargs)

    @classmethod
    def from_bytes(cls, data: bytes, mime_type: str = "image/jpeg", **kwargs: Any) -> "ImageAnalysisRequest":
        return cls(image_bytes=data, source_type=ImageSourceType.BYTES, mime_type=mime_type, **kwargs)


@dataclass
class LabelResult:
    """A single detected label with confidence and bounding information."""

    label: str
    confidence: float
    mid: Optional[str] = None
    bounding_poly: Optional[Dict[str, Any]] = None
    localization_metadata: Optional[Dict[str, Any]] = None


@dataclass
class LabelDetectionResponse:
    """Container for label detection output."""

    labels: List[LabelResult] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None


@dataclass
class TextDetectionResult:
    """A single detected text block or word."""

    text: str
    confidence: float
    bounding_box: Optional[List[Dict[str, int]]] = None
    language: Optional[str] = None
    block_type: str = "word"


@dataclass
class TextDetectionResponse:
    """Container for text (OCR) detection output."""

    texts: List[TextDetectionResult] = field(default_factory=list)
    full_text: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyRating:
    """Safety category rating for an image."""

    category: str
    likelihood: str
    likelihood_score: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class SafetyScoreResponse:
    """Container for safety scoring output."""

    ratings: List[SafetyRating] = field(default_factory=list)
    is_safe: bool = True
    flagged_categories: List[str] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ImageDescription:
    """Generated visual description for an image."""

    description: str
    confidence: float
    topics: List[str] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


def normalize_labels_from_gcloud(
    response: Any, max_results: int = 10
) -> LabelDetectionResponse:
    """Normalize Google Cloud Vision label detection response."""
    labels = []
    for label_annotation in getattr(response, "label_annotations", [])[:max_results]:
        labels.append(
            LabelResult(
                label=label_annotation.description,
                confidence=label_annotation.score,
                mid=label_annotation.mid,
            )
        )
    return LabelDetectionResponse(labels=labels, raw_response={"status": "ok"})


def normalize_text_from_gcloud(response: Any) -> TextDetectionResponse:
    """Normalize Google Cloud Vision text detection response."""
    texts: List[TextDetectionResult] = []
    full_parts: List[str] = []
    for page in getattr(response, "full_text_annotation", {}).pages if hasattr(response, "full_text_annotation") else []:
        for block in getattr(page, "blocks", []):
            for paragraph in getattr(block, "paragraphs", []):
                for word in getattr(paragraph, "words", []):
                    word_text = "".join(
                        symbol.text
                        for symbol in getattr(word, "symbols", [])
                    )
                    confidence = getattr(word, "confidence", 1.0)
                    texts.append(
                        TextDetectionResult(
                            text=word_text,
                            confidence=confidence,
                            block_type="word",
                        )
                    )
                    full_parts.append(word_text)
    full_text = " ".join(full_parts)
    return TextDetectionResponse(texts=texts, full_text=full_text)


def normalize_safety_from_gcloud(response: Any) -> SafetyScoreResponse:
    """Normalize Google Cloud Vision safe search detection response."""
    ratings: List[SafetyRating] = []
    flagged: List[str] = []
    safe_search = getattr(response, "safe_search_annotation", None)
    if safe_search:
        likelihood_map = {
            "VERY_UNLIKELY": 0.0,
            "UNLIKELY": 0.2,
            "POSSIBLE": 0.5,
            "LIKELY": 0.8,
            "VERY_LIKELY": 1.0,
        }
        categories = [
            ("adult", safe_search.adult),
            ("violence", safe_search.violence),
            ("racy", safe_search.racy),
            ("spoof", safe_search.spoof),
            ("medical", safe_search.medical),
        ]
        for cat_name, likelihood in categories:
            likelihood_str = str(likelihood).split(".")[-1].upper()
            score = likelihood_map.get(likelihood_str, 0.5)
            rating = SafetyRating(
                category=cat_name,
                likelihood=likelihood_str,
                likelihood_score=score,
            )
            ratings.append(rating)
            if score >= 0.5:
                flagged.append(cat_name)
    is_safe = len(flagged) == 0
    return SafetyScoreResponse(
        ratings=ratings, is_safe=is_safe, flagged_categories=flagged
    )


def normalize_description_from_gcloud(response: Any) -> ImageDescription:
    """Normalize Google Cloud Vision image annotation description."""
    descriptions: List[str] = []
    confidences: List[float] = []
    for desc in getattr(response, "label_annotations", [])[:3]:
        descriptions.append(desc.description)
        confidences.append(desc.score)
    caption = ", ".join(descriptions) if descriptions else ""
    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
    return ImageDescription(
        description=caption,
        confidence=avg_conf,
        topics=descriptions,
    )


def _guess_mime(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    return mime_map.get(ext, "image/jpeg")


def encode_image_bytes(image_bytes: bytes) -> str:
    """Base64-encode image bytes for API payloads."""
    return base64.b64encode(image_bytes).decode("utf-8")
