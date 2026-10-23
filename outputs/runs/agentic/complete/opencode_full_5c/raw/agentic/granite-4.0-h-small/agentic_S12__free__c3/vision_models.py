# vision_models.py
# [HELPER]

from typing import Any, Dict, List, Optional

# Normalized response models for vision tasks


class LabelResponse:
    """Labels/objects detected in an image."""

    def __init__(self, items: List[Dict[str, Any]]):
        self.labels = items  # [{'name': 'cat', 'confidence': 0.96}, ...]


class CaptionResponse:
    """Generated short visual description."""

    def __init__(self, text: str):
        self.caption = text


class OcrResponse:
    """Extracted text from an image."""

    def __init__(self, lines: List[Dict[str, Any]]):
        self.lines = lines  # [{'boundingBox': {...}, 'text': 'Hello'}]


class SafetyCheckResponse:
    """Safety evaluation result."""

    def __init__(self, flags: Dict[str, str]):
        self.adult = flags.get("adult", "UNLIKELY")
        self.violence = flags.get("violence", "UNLIKELY")
        self.medical = flags.get("medical", "UNLIKELY")
        self.racy = flags.get("racy", "UNLIKELY")


def normalize_labels(raw: Dict[str, Any]) -> LabelResponse:
    """Convert raw provider response to normalized LabelResponse."""
    # Example AWS Rekognition: raw['Labels'] returns list of dicts
    items = raw.get("Labels", [])
    return LabelResponse(items)


def normalize_caption(raw: str) -> CaptionResponse:
    """Normalize raw caption string into CaptionResponse."""
    return CaptionResponse(raw)


def extract_ocr_text(raw: Dict[str, Any]) -> OcrResponse:
    """Normalize raw OCR response into OcrResponse."""
    lines = []
    if "fullTextAnnotation" in raw:
        # Generic placeholder for Google Vision response
        for block in raw["fullTextAnnotation"].get("blocks", []):
            text = block.get("content", "")
            lines.append({"boundingBox": {}, "text": text})
    elif "recognitionResults" in raw:
        # Azure OCR format
        for line in raw["recognitionResults"][0].get("lines", []):
            lines.append({"boundingBox": {}, "text": line["text"]})
    else:
        # Fallback empty
        lines = []
    return OcrResponse(lines)


def normalize_safety_check(raw: Dict[str, Any]) -> SafetyCheckResponse:
    """Normalize raw SafeSearch response into SafetyCheckResponse."""
    flags = {
        "adult": raw.get("safeSearchAnnotation", {}).get("adult", "UNLIKELY"),
        "violence": raw.get("safeSearchAnnotation", {}).get("violence", "UNLIKELY"),
        "medical": raw.get("safeSearchAnnotation", {}).get("medical", "UNLIKELY"),
        "racy": raw.get("safeSearchAnnotation", {}).get("racy", "UNLIKELY"),
    }
    return SafetyCheckResponse(flags)
