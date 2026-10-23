from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ImageRequest:
    image_path: str
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/jpeg"


@dataclass
class LabelEntry:
    label: str
    confidence: float
    category: str = ""


@dataclass
class LabelDetectionResult:
    image_path: str
    labels: list[LabelEntry] = field(default_factory=list)


@dataclass
class ImageDescriptionResult:
    image_path: str
    description: str = ""
    confidence: float = 0.0


@dataclass
class TextAnnotation:
    text: str
    confidence: float
    bounding_box: Optional[dict] = None


@dataclass
class TextDetectionResult:
    image_path: str
    annotations: list[TextAnnotation] = field(default_factory=list)
    full_text: str = ""


@dataclass
class SafetyScores:
    adult: float = 0.0
    violence: float = 0.0
    racy: float = 0.0
    medical: float = 0.0
    spoof: float = 0.0


@dataclass
class SafetyCheckResult:
    image_path: str
    scores: SafetyScores = field(default_factory=SafetyScores)
    is_safe: bool = True


@dataclass
class VisualAnalysisSummary:
    image_path: str
    description: str = ""
    labels: list[str] = field(default_factory=list)
    detected_text: str = ""
    safety_is_safe: bool = True
    summary: str = ""


@dataclass
class TranslatedAltText:
    original: str
    translated: str
    target_language: str


@dataclass
class TextSafetyResult:
    text: str
    is_safe: bool = True
    categories: dict = field(default_factory=dict)


@dataclass
class ArchiveManifest:
    image_path: str
    archive_key: str
    uploaded_objects: list[str] = field(default_factory=list)


def normalize_confidence(raw_score: float) -> float:
    return round(min(max(raw_score, 0.0), 1.0), 4)


def normalize_labels(raw_labels: list[dict]) -> list[LabelEntry]:
    return [
        LabelEntry(
            label=item.get("label", item.get("description", "")),
            confidence=normalize_confidence(
                item.get("confidence", item.get("score", 0.0))
            ),
            category=item.get("category", ""),
        )
        for item in raw_labels
    ]


def build_full_text(annotations: list[TextAnnotation]) -> str:
    return " ".join(a.text for a in annotations).strip()


def evaluate_safety(scores: SafetyScores, threshold: float = 0.6) -> bool:
    return all(
        getattr(scores, attr) < threshold
        for attr in ("adult", "violence", "racy", "medical", "spoof")
    )
