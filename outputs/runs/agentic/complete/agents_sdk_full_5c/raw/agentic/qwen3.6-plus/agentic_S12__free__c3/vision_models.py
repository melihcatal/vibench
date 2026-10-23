"""
Local request, response, and normalization helpers for Static Image and Visual Understanding.
Defines Pydantic models and utility functions for payload normalization and response parsing.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    SELF_HARM = "self_harm"
    SEXUAL = "sexual"
    VIOLENCE = "violence"


@dataclass
class ImageLabel:
    """Represents a detected label or object in an image."""
    name: str
    confidence: float
    instances: List[Dict[str, int]] = field(default_factory=list)
    parents: List[str] = field(default_factory=list)

    @classmethod
    def from_rekognition(cls, label_data: dict) -> "ImageLabel":
        """Parse AWS Rekognition label response."""
        return cls(
            name=label_data.get("Name", ""),
            confidence=label_data.get("Confidence", 0.0),
            instances=[
                {
                    "x": int(i.get("BoundingBox", {}).get("Left", 0) * 100),
                    "y": int(i.get("BoundingBox", {}).get("Top", 0) * 100),
                    "width": int(i.get("BoundingBox", {}).get("Width", 0) * 100),
                    "height": int(i.get("BoundingBox", {}).get("Height", 0) * 100),
                }
                for i in label_data.get("Instances", [])
            ],
            parents=[p.get("Name", "") for p in label_data.get("Parents", [])],
        )

    @classmethod
    def from_google_vision(cls, entity_annotation) -> "ImageLabel":
        """Parse Google Cloud Vision label/entity response."""
        return cls(
            name=entity_annotation.description,
            confidence=entity_annotation.score,
            parents=[
                p.description for p in getattr(entity_annotation, "web_entities", [])
            ],
        )


@dataclass
class ImageDescription:
    """Represents a generated visual description for an image."""
    text: str
    model_used: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @classmethod
    def from_openai_response(cls, response) -> "ImageDescription":
        """Parse OpenAI GPT-4 vision response."""
        choice = response.choices[0]
        return cls(
            text=choice.message.content or "",
            model_used=response.model,
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
        )


@dataclass
class DetectedText:
    """Represents detected text within an image."""
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, int]] = None
    language: str = "en"

    @classmethod
    def from_google_vision(cls, text_annotation) -> "DetectedText":
        """Parse Google Cloud Vision OCR text annotation."""
        bounds = text_annotation.bounding_poly.vertices if hasattr(text_annotation, "bounding_poly") else None
        box = None
        if bounds:
            box = {
                "x": bounds[0].x if bounds else 0,
                "y": bounds[0].y if bounds else 0,
                "width": bounds[2].x - bounds[0].x if len(bounds) > 2 else 0,
                "height": bounds[2].y - bounds[0].y if len(bounds) > 2 else 0,
            }
        return cls(
            text=text_annotation.description,
            confidence=text_annotation.confidence if hasattr(text_annotation, "confidence") else 1.0,
            bounding_box=box,
            language=text_annotation.locale if hasattr(text_annotation, "locale") else "en",
        )


@dataclass
class SafetyResult:
    """Represents image safety analysis results."""
    category: SafetyCategory
    severity: int  # 0-7 scale
    is_flagged: bool
    details: Optional[str] = None

    @classmethod
    def from_azure_response(cls, category_name: str, severity: int, threshold: int = 4) -> "SafetyResult":
        """Parse Azure Content Safety response into normalized SafetyResult."""
        cat_map = {
            "Hate": SafetyCategory.HATE,
            "SelfHarm": SafetyCategory.SELF_HARM,
            "Sexual": SafetyCategory.SEXUAL,
            "Violence": SafetyCategory.VIOLENCE,
        }
        return cls(
            category=cat_map.get(category_name, SafetyCategory.VIOLENCE),
            severity=severity,
            is_flagged=severity >= threshold,
        )


@dataclass
class ImageAnalysisPayload:
    """Container for image analysis request/response data."""
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    labels: List[ImageLabel] = field(default_factory=list)
    description: Optional[ImageDescription] = None
    detected_texts: List[DetectedText] = field(default_factory=list)
    safety_results: List[SafetyResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_labels(self) -> bool:
        return len(self.labels) > 0

    def has_safety_flags(self) -> bool:
        return any(r.is_flagged for r in self.safety_results)

    def get_text_content(self) -> str:
        """Extract all detected text as a single string."""
        return " ".join(dt.text for dt in self.detected_texts)

    def to_summary_dict(self) -> Dict[str, Any]:
        """Convert to a summary dictionary for downstream processing."""
        return {
            "labels": [{"name": l.name, "confidence": l.confidence} for l in self.labels],
            "description": self.description.text if self.description else None,
            "detected_texts": [dt.text for dt in self.detected_texts],
            "safety_flags": [
                {"category": r.category.value, "severity": r.severity}
                for r in self.safety_results if r.is_flagged
            ],
            "metadata": self.metadata,
        }


def normalize_confidence_scores(items: List[Any], threshold: float = 0.7) -> List[Any]:
    """Filter items by confidence threshold."""
    return [item for item in items if getattr(item, "confidence", 0.0) >= threshold]


def merge_label_results(results: List[List[ImageLabel]]) -> List[ImageLabel]:
    """Merge and deduplicate label results from multiple providers."""
    seen = {}
    for label_list in results:
        for label in label_list:
            if label.name not in seen:
                seen[label.name] = label
            elif label.confidence > seen[label.name].confidence:
                seen[label.name] = label
    return list(seen.values())
