"""
vision_models.py - Define local request, response, and normalization helpers
for Static Image and Visual Understanding tasks using Google Cloud Vision API.

Provider: Google Cloud Vision API (vision.googleapis.com)
Provider SDK: google-cloud-vision
Provider Identifying Signals: google.cloud.vision_v1.ImageAnnotatorClient,
                              vision.googleapis.com hostname references,
                              GCLOUD_VISION_ env vars
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import os
import base64


@dataclass
class VisionImageRequest:
    """Normalized request wrapper for static image input."""
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    image_uri: Optional[str] = None
    mime_type: Optional[str] = None

    def __post_init__(self):
        if self.image_path and not self.image_bytes:
            with open(self.image_path, "rb") as f:
                self.image_bytes = f.read()
            if not self.mime_type:
                ext = os.path.splitext(self.image_path)[-1].lower()
                self.mime_type = {
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".gif": "image/gif",
                    ".webp": "image/webp",
                    ".bmp": "image/bmp",
                }.get(ext, "image/jpeg")

    def to_gcs_image_source(self) -> Dict[str, Any]:
        """Convert to Google Cloud Vision ImageSource format for GCS URIs."""
        if self.image_uri:
            return {"gcs_image_uri": self.image_uri}
        raise ValueError("No GCS URI available for ImageSource")

    def to_bytes_content(self) -> Dict[str, Any]:
        """Convert to raw bytes content for direct API calls."""
        if self.image_bytes:
            return {"content": self.image_bytes}
        raise ValueError("No image bytes available")


@dataclass
class ImageLabel:
    """Normalized label detection result."""
    description: str
    score: float
    confidence: float
    topicality: float = 0.0
    mid: Optional[str] = None

    @classmethod
    def from_google_label(cls, google_label) -> "ImageLabel":
        """Normalize from google.cloud.vision_v1.EntityAnnotation."""
        return cls(
            description=google_label.description,
            score=google_label.score,
            confidence=getattr(google_label, "confidence", google_label.score),
            topicality=getattr(google_label, "topicality", 0.0),
            mid=getattr(google_label, "mid", None),
        )


@dataclass
class DetectedText:
    """Normalized text detection result (OCR)."""
    text: str
    confidence: float
    bounding_poly: Optional[List[Dict[str, int]]] = None
    language: Optional[str] = None

    @classmethod
    def from_google_text(cls, google_annotation) -> "DetectedText":
        """Normalize from google.cloud.vision_v1.EntityAnnotation (TEXT_DETECTION)."""
        bounding = None
        if hasattr(google_annotation, "bounding_poly") and google_annotation.bounding_poly:
            bounding = [
                {"x": vertex.x, "y": vertex.y}
                for vertex in google_annotation.bounding_poly.vertices
            ]
        return cls(
            text=google_annotation.description,
            confidence=google_annotation.score,
            bounding_poly=bounding,
            language=getattr(google_annotation, "locale", None),
        )


@dataclass
class SafetyRating:
    """Normalized safety/policy rating result."""
    category: str
    likelihood: str
    likelihood_score: float

    @classmethod
    def from_google_safe_search(cls, category_name: str, likelihood_name: str) -> "SafetyRating":
        """Normalize from Google Cloud Vision SafeSearchAnnotation."""
        likelihood_map = {
            "VERY_UNLIKELY": 0.0,
            "UNLIKELY": 0.2,
            "POSSIBLE": 0.5,
            "LIKELY": 0.8,
            "VERY_LIKELY": 1.0,
        }
        return cls(
            category=category_name,
            likelihood=likelihood_name,
            likelihood_score=likelihood_map.get(likelihood_name, 0.0),
        )


@dataclass
class ImageLabelsResponse:
    """Response container for label detection."""
    labels: List[ImageLabel] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def top_labels(self, n: int = 5) -> List[ImageLabel]:
        """Return top N labels sorted by score."""
        return sorted(self.labels, key=lambda l: l.score, reverse=True)[:n]

    def has_label(self, keyword: str, threshold: float = 0.5) -> bool:
        """Check if a label matching keyword exists above threshold."""
        keyword_lower = keyword.lower()
        return any(
            l.score >= threshold and keyword_lower in l.description.lower()
            for l in self.labels
        )


@dataclass
class ImageDescriptionResponse:
    """Response container for image description."""
    description: str
    confidence: float
    topics: List[str] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class ImageTextResponse:
    """Response container for text detection (OCR)."""
    texts: List[DetectedText] = field(default_factory=list)
    full_text: str = ""
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def contains_keyword(self, keyword: str, case_sensitive: bool = False) -> bool:
        """Check if detected text contains a keyword."""
        search_text = self.full_text if case_sensitive else self.full_text.lower()
        search_keyword = keyword if case_sensitive else keyword.lower()
        return search_keyword in search_text


@dataclass
class ImageSafetyResponse:
    """Response container for safety/policy analysis."""
    ratings: List[SafetyRating] = field(default_factory=list)
    is_safe: bool = True
    flagged_categories: List[str] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def is_unsafe(self, threshold: float = 0.5) -> bool:
        """Check if any category exceeds the safety threshold."""
        return any(r.likelihood_score >= threshold for r in self.ratings)

    def get_violations(self, threshold: float = 0.5) -> List[SafetyRating]:
        """Return categories that violate the safety threshold."""
        return [r for r in self.ratings if r.likelihood_score >= threshold]


def encode_image_base64(image_path: str) -> str:
    """Encode an image file to base64 string for API transmission."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def normalize_google_response(raw_response: Any) -> Dict[str, Any]:
    """Normalize a Google Cloud Vision API response to a plain dict."""
    if hasattr(raw_response, "SerializeToString"):
        import json
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(raw_response._pb)
    return dict(raw_response)
