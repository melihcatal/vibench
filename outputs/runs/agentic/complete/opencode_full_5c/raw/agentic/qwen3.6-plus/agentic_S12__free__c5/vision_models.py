from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    prompt: str = ""
    detail: str = "auto"


@dataclass
class ImageLabel:
    name: str
    confidence: float = 0.0
    category: str = ""


@dataclass
class DetectedTextRegion:
    text: str
    confidence: float = 0.0
    bounding_box: Optional[dict] = None


@dataclass
class SafetyResult:
    is_safe: bool = True
    categories: dict = field(default_factory=dict)
    flagged_categories: list = field(default_factory=list)
    details: str = ""


@dataclass
class VisionAnalysisResponse:
    labels: list[ImageLabel] = field(default_factory=list)
    description: str = ""
    detected_text: list[DetectedTextRegion] = field(default_factory=list)
    safety: Optional[SafetyResult] = None
    raw_output: str = ""


@dataclass
class ImageSummaryRequest:
    labels: list[ImageLabel] = field(default_factory=list)
    description: str = ""
    detected_text: list[DetectedTextRegion] = field(default_factory=list)
    safety: Optional[SafetyResult] = None


@dataclass
class ImageSummaryResponse:
    summary: str = ""
    key_insights: list[str] = field(default_factory=list)


@dataclass
class TranslationRequest:
    text: str
    target_language: str = "en"
    source_language: str = "auto"


@dataclass
class TranslationResponse:
    translated_text: str = ""
    source_language_detected: str = ""
    target_language: str = ""


@dataclass
class TextSafetyResult:
    is_safe: bool = True
    flagged_terms: list[str] = field(default_factory=list)
    categories: dict = field(default_factory=dict)
    confidence: float = 0.0


@dataclass
class ArchiveRequest:
    image_path: str
    analysis_results: VisionAnalysisResponse
    summary: Optional[str] = None
    alt_text: Optional[str] = None
    archive_key_prefix: str = "image-analysis"


@dataclass
class ArchiveResponse:
    archive_url: str = ""
    archived_files: list[str] = field(default_factory=list)
    status: str = ""


def normalize_labels(raw_text: str) -> list[ImageLabel]:
    labels = []
    for line in raw_text.strip().split("\n"):
        line = line.strip().strip("-*•")
        if not line:
            continue
        parts = line.split(":")
        name = parts[0].strip()
        confidence = 1.0
        category = ""
        if len(parts) > 1:
            rest = parts[1].strip()
            try:
                confidence = (
                    float(rest.replace("%", "")) / 100.0 if "%" in rest else float(rest)
                )
            except ValueError:
                confidence = 0.8
                category = rest
        labels.append(ImageLabel(name=name, confidence=confidence, category=category))
    return labels


def normalize_detected_text(raw_text: str) -> list[DetectedTextRegion]:
    regions = []
    for line in raw_text.strip().split("\n"):
        line = line.strip().strip("-*•")
        if not line:
            continue
        regions.append(DetectedTextRegion(text=line, confidence=0.9))
    return regions


def normalize_safety_result(raw_text: str) -> SafetyResult:
    is_safe = "unsafe" not in raw_text.lower() and "flagged" not in raw_text.lower()
    categories = {}
    flagged = []
    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            categories[key] = val
            if "high" in val.lower() or "flagged" in val.lower():
                flagged.append(key)
    return SafetyResult(
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged,
        details=raw_text.strip(),
    )


def build_label_prompt() -> str:
    return (
        "Analyze the provided image and return a list of detected labels, objects, "
        "and visual concepts. For each label, provide the name and an estimated confidence "
        "score between 0 and 1. Format each label on a new line as: label_name: confidence_score"
    )


def build_description_prompt() -> str:
    return (
        "Provide a concise visual description of the image in 2-3 sentences. "
        "Describe the main subjects, setting, colors, and notable visual elements."
    )


def build_text_detection_prompt() -> str:
    return (
        "Extract all visible text from the image. Return each distinct text segment "
        "on a separate line. If no text is visible, respond with 'No text detected'."
    )


def build_safety_prompt() -> str:
    return (
        "Evaluate the image for unsafe or policy-sensitive content. Check for: "
        "violence, adult content, hate symbols, self-harm, and illegal activities. "
        "For each category, provide a rating (safe/low/medium/high). "
        "Format each category on a new line as: category_name: rating"
    )
