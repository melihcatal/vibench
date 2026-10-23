# [HELPER] vision_models.py

import dataclasses
from typing import Any, List, Dict


dataclass
class LabelAnnotation:
    description: str
    score: float = 0.0

@dataclass
class Caption:
    text: str
    confidence: float = 0.0

@dataclass
class TextAnnotation:
    description: str

@dataclass
class UnsafeCategory:
    category: str
    score: float

@dataclass
class VisionResponseNormalization:
    labels: List[LabelAnnotation] = dataclasses.field(default_factory=list)
    captions: List[Caption] = dataclasses.field(default_factory=list)
    texts: List[TextAnnotation] = dataclasses.field(default_factory=list)
    unsafe: List[UnsafeCategory] = dataclasses.field(default_factory=list)
    
    @classmethod
def from_provider_response(cls, provider_response: Any) -> "VisionResponseNormalization":
        norm = cls()
        # Generic mapping - implementations per provider can be added as needed.
        if isinstance(provider_response, list) and isinstance(provider_response[0], dict):
            # Assume list of label dicts with 'description' and 'score'
            norm.labels = [LabelAnnotation(**lbl) for lbl in provider_response]
        elif hasattr(provider_response, "get"):
            # Assume dict-like with known keys
            for caption in provider_response.get("captions", []):
                norm.captions.append(Caption(text=caption.get("text"), confidence=caption.get("confidence", 0.0)))
            for txt in provider_response.get("textAnnotations", []):
                norm.texts.append(TextAnnotation(description=txt.get("description", "")))
            for unsafe in provider_response.get("detectedUnsafe", []):
                norm.unsafe.append(UnsafeCategory(category=unsafe.get("category"), score=unsafe.get("score", 0.0)))
        return norm


def normalize_vision_response(provider_response: Any) -> VisionResponseNormalization:
    """Convert raw provider response into a consistent internal model."""
    return VisionResponseNormalization.from_provider_response(provider_response)
