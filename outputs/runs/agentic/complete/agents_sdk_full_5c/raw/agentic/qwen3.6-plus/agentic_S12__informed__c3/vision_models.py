"""Local request, response, and normalization helpers for Static Image and Visual Understanding.

Provides dataclasses and utility functions for normalizing Google Cloud Vision API responses
into a unified internal schema.

Provider: Google Cloud Vision
SDK: google-cloud-vision
"""

from dataclasses import dataclass, field
from typing import List, Optional

from google.cloud import vision as google_vision


@dataclass
class ImageLabel:
    """Normalized label detected in an image."""

    name: str
    confidence: float
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "confidence": self.confidence,
            "description": self.description,
        }


@dataclass
class ImageTextAnnotation:
    """Normalized text detected inside an image."""

    text: str
    confidence: float
    bounding_box: Optional[List[List[int]]] = None
    locale: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box,
            "locale": self.locale,
        }


@dataclass
class ImageSafetyScore:
    """Normalized safety / moderation scores for an image."""

    adult: float = 0.0
    spoof: float = 0.0
    medical: float = 0.0
    violence: float = 0.0
    racy: float = 0.0

    @property
    def max_risk(self) -> float:
        """Return the highest risk score across all categories."""
        return max(
            self.adult, self.spoof, self.medical, self.violence, self.racy
        )

    @property
    def is_safe(self) -> bool:
        """Return True when the maximum risk score is below 0.5."""
        return self.max_risk < 0.5

    def to_dict(self) -> dict:
        return {
            "adult": self.adult,
            "spoof": self.spoof,
            "medical": self.medical,
            "violence": self.violence,
            "racy": self.racy,
            "is_safe": self.is_safe,
            "max_risk": self.max_risk,
        }


@dataclass
class ImageDescription:
    """Normalized description of an image."""

    text: str
    confidence: float
    labels: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "labels": self.labels,
        }


def normalize_label_results(
    response: google_vision.AnnotateImageResponse,
) -> List[ImageLabel]:
    """Convert Google Cloud Vision label detection results to normalized labels."""
    labels = []
    for label in response.label_annotations:
        labels.append(
            ImageLabel(
                name=label.description,
                confidence=label.score,
                description=label.description,
            )
        )
    return labels


def normalize_text_detection_results(
    response: google_vision.AnnotateImageResponse,
) -> List[ImageTextAnnotation]:
    """Convert Google Cloud Vision text detection results to normalized annotations."""
    annotations = []
    for annotation in response.text_annotations:
        box = None
        if annotation.bounding_poly and annotation.bounding_poly.vertices:
            box = [
                [vertex.x, vertex.y]
                for vertex in annotation.bounding_poly.vertices
            ]
        annotations.append(
            ImageTextAnnotation(
                text=annotation.description,
                confidence=annotation.confidence if hasattr(annotation, "confidence") else 1.0,
                bounding_box=box,
                locale=getattr(annotation, "locale", None),
            )
        )
    return annotations


def normalize_safe_search_results(
    response: google_vision.AnnotateImageResponse,
) -> ImageSafetyScore:
    """Convert Google Cloud Vision safe search results to a normalized score."""
    safe_props = response.safe_search_annotation
    likelihood_map = {
        google_vision.Likelihood.UNKNOWN: 0.0,
        google_vision.Likelihood.VERY_UNLIKELY: 0.1,
        google_vision.Likelihood.UNLIKELY: 0.3,
        google_vision.Likelihood.POSSIBLE: 0.5,
        google_vision.Likelihood.LIKELY: 0.8,
        google_vision.Likelihood.VERY_LIKELY: 1.0,
    }
    return ImageSafetyScore(
        adult=likelihood_map.get(safe_props.adult, 0.0) if safe_props else 0.0,
        spoof=likelihood_map.get(safe_props.spoof, 0.0) if safe_props else 0.0,
        medical=likelihood_map.get(safe_props.medical, 0.0) if safe_props else 0.0,
        violence=likelihood_map.get(safe_props.violence, 0.0) if safe_props else 0.0,
        racy=likelihood_map.get(safe_props.racy, 0.0) if safe_props else 0.0,
    )


def normalize_web_description_results(
    response: google_vision.AnnotateImageResponse,
) -> ImageDescription:
    """Build a short description from Google Cloud Vision web detection best guesses."""
    best_guess_labels = response.web_detection.best_guess_labels
    labels_list = [lbl.label for lbl in response.web_detection.web_entities]

    description_text = ", ".join([lbl.label for lbl in best_guess_labels])
    confidence = best_guess_labels[0].score if best_guess_labels else 0.0

    return ImageDescription(
        text=description_text,
        confidence=confidence,
        labels=labels_list,
    )


def build_label_detection_request(
    image: google_vision.Image,
    max_results: int = 10,
) -> google_vision.AnnotateImageRequest:
    """Build a Google Cloud Vision label detection request."""
    feature = google_vision.Feature(
        type_=google_vision.Feature.Type.LABEL_DETECTION,
        max_results=max_results,
    )
    return google_vision.AnnotateImageRequest(image=image, features=[feature])


def build_text_detection_request(
    image: google_vision.Image,
) -> google_vision.AnnotateImageRequest:
    """Build a Google Cloud Vision text detection request."""
    feature = google_vision.Feature(
        type_=google_vision.Feature.Type.TEXT_DETECTION,
    )
    return google_vision.AnnotateImageRequest(image=image, features=[feature])


def build_safe_search_request(
    image: google_vision.Image,
) -> google_vision.AnnotateImageRequest:
    """Build a Google Cloud Vision safe search detection request."""
    feature = google_vision.Feature(
        type_=google_vision.Feature.Type.SAFE_SEARCH_DETECTION,
    )
    return google_vision.AnnotateImageRequest(image=image, features=[feature])


def build_image_description_request(
    image: google_vision.Image,
) -> google_vision.AnnotateImageRequest:
    """Build a Google Cloud Vision web detection request for image description."""
    feature = google_vision.Feature(
        type_=google_vision.Feature.Type.WEB_DETECTION,
    )
    return google_vision.AnnotateImageRequest(image=image, features=[feature])
