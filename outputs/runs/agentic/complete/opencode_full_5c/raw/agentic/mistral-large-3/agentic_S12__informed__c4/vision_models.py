from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class LabelDetectionResponse:
    labels: List[Dict[str, Any]]


@dataclass
class ImageDescriptionResponse:
    description: str
    dominant_colors: List[Dict[str, Any]]


@dataclass
class TextDetectionResponse:
    texts: List[Dict[str, Any]]


@dataclass
class ImageSafetyResponse:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


def normalize_label_annotation(labels) -> LabelDetectionResponse:
    """Normalizes label annotations from Google Cloud Vision API."""
    normalized_labels = [
        {
            "description": label.description,
            "score": label.score,
            "topicality": label.topicality,
        }
        for label in labels
    ]
    return LabelDetectionResponse(labels=normalized_labels)


def normalize_image_description(
    dominant_colors: List[Dict[str, Any]], description: float
) -> ImageDescriptionResponse:
    """Normalizes image description data from Google Cloud Vision API."""
    return ImageDescriptionResponse(
        description=f"Image with dominant colors and confidence score: {description}",
        dominant_colors=dominant_colors,
    )


def normalize_text_annotation(texts) -> TextDetectionResponse:
    """Normalizes text annotations from Google Cloud Vision API."""
    normalized_texts = [
        {
            "description": text.description,
            "bounding_poly": {
                "vertices": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in text.bounding_poly.vertices
                ]
            },
        }
        for text in texts
    ]
    return TextDetectionResponse(texts=normalized_texts)


def normalize_safety_annotation(safe_search) -> ImageSafetyResponse:
    """Normalizes safety annotations from Google Cloud Vision API."""
    return ImageSafetyResponse(
        adult=str(safe_search.adult),
        spoof=str(safe_search.spoof),
        medical=str(safe_search.medical),
        violence=str(safe_search.violence),
        racy=str(safe_search.racy),
    )
