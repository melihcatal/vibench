from typing import List, Dict, NamedTuple, Optional


class LabelDetectionResponse(NamedTuple):
    """Response model for label detection."""

    labels: List[str]


class ImageDescriptionResponse(NamedTuple):
    """Response model for image description."""

    description: str


class TextDetectionResponse(NamedTuple):
    """Response model for text detection."""

    texts: List[str]


class SafetyScoreResponse(NamedTuple):
    """Response model for image safety scoring."""

    score: float
    reason: str


def normalize_labels(labels: List[Dict]) -> List[str]:
    """Normalizes label detection results into a list of strings."""
    normalized = []
    for label in labels:
        if isinstance(label, dict) and "text" in label:
            normalized.extend(
                [l.strip() for l in label["text"].split(",") if l.strip()]
            )
        elif isinstance(label, str):
            normalized.extend([l.strip() for l in label.split(",") if l.strip()])
    return normalized


def normalize_texts(texts: List[Dict]) -> List[str]:
    """Normalizes text detection results into a list of strings."""
    normalized = []
    for text in texts:
        if isinstance(text, dict) and "text" in text:
            normalized.extend(
                [t.strip() for t in text["text"].split("\n") if t.strip()]
            )
        elif isinstance(text, str):
            normalized.extend([t.strip() for t in text.split("\n") if t.strip()])
    return normalized
