from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ImageLabel:
    name: str
    confidence: float
    category: Optional[str] = None


@dataclass
class DetectedText:
    text: str
    bounding_box: Optional[Dict[str, float]] = None
    confidence: float = 1.0


@dataclass
class SafetyScore:
    is_safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    overall_score: float = 0.0
    flagged_categories: List[str] = field(default_factory=list)


@dataclass
class ImageDescription:
    description: str
    summary: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class VisionAnalysisResult:
    labels: List[ImageLabel] = field(default_factory=list)
    description: Optional[ImageDescription] = None
    detected_texts: List[DetectedText] = field(default_factory=list)
    safety: Optional[SafetyScore] = None


def normalize_labels(raw_text: str) -> List[ImageLabel]:
    labels = []
    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        name = parts[0].strip()
        confidence = 0.9
        category = None
        if len(parts) >= 2:
            try:
                confidence = float(parts[1].strip())
            except ValueError:
                category = parts[1].strip()
        if len(parts) >= 3:
            category = parts[2].strip()
        labels.append(ImageLabel(name=name, confidence=confidence, category=category))
    return labels


def normalize_description(raw_text: str) -> ImageDescription:
    return ImageDescription(description=raw_text.strip())


def normalize_detected_text(raw_text: str) -> List[DetectedText]:
    texts = []
    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if line:
            texts.append(DetectedText(text=line))
    return texts


def normalize_safety_score(raw_text: str) -> SafetyScore:
    categories = {}
    flagged = []
    is_safe = True
    overall_score = 1.0
    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            try:
                score = float(val.strip())
            except ValueError:
                continue
            categories[key] = score
            if score > 0.5:
                is_safe = False
                flagged.append(key)
    if categories:
        overall_score = (
            min(categories.values()) if not is_safe else max(categories.values())
        )
    return SafetyScore(
        is_safe=is_safe,
        categories=categories,
        overall_score=overall_score,
        flagged_categories=flagged,
    )


def build_analysis_result(
    labels_raw: Optional[str] = None,
    description_raw: Optional[str] = None,
    text_raw: Optional[str] = None,
    safety_raw: Optional[str] = None,
) -> VisionAnalysisResult:
    result = VisionAnalysisResult()
    if labels_raw:
        result.labels = normalize_labels(labels_raw)
    if description_raw:
        result.description = normalize_description(description_raw)
    if text_raw:
        result.detected_texts = normalize_detected_text(text_raw)
    if safety_raw:
        result.safety = normalize_safety_score(safety_raw)
    return result
