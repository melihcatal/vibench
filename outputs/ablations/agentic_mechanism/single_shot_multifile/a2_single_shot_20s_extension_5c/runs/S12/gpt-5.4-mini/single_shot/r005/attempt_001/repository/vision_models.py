from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageLabel:
    description: str
    score: float


@dataclass
class ImageText:
    text: str
    confidence: Optional[float] = None


@dataclass
class SafetyScore:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


def _safe_enum(value: Any) -> str:
    return getattr(value, "name", str(value))


def normalize_label_response(response: Any, image_path: str, provider: str, kind: str) -> Dict[str, Any]:
    labels = []
    for ann in getattr(response, "label_annotations", []) or []:
        labels.append({"description": getattr(ann, "description", ""), "score": float(getattr(ann, "score", 0.0))})
    return {"provider": provider, "kind": kind, "image_path": image_path, "labels": labels}


def normalize_description_response(image_path: str, properties: Any, labels: Any, objects: Any, provider: str) -> Dict[str, Any]:
    desc = []
    for ann in getattr(labels, "label_annotations", []) or []:
        desc.append(getattr(ann, "description", ""))
    return {"provider": provider, "image_path": image_path, "description": ", ".join(desc[:3]), "raw": {"properties": str(properties), "objects": str(objects)}}


def normalize_text_response(response: Any, image_path: str, provider: str) -> Dict[str, Any]:
    texts = []
    for ann in getattr(response, "text_annotations", []) or []:
        texts.append(getattr(ann, "description", ""))
    return {"provider": provider, "image_path": image_path, "texts": texts}


def normalize_safety_response(response: Any, image_path: str, provider: str) -> Dict[str, Any]:
    annotation = getattr(response, "safe_search_annotation", None)
    return {
        "provider": provider,
        "image_path": image_path,
        "adult": _safe_enum(getattr(annotation, "adult", "UNKNOWN")),
        "spoof": _safe_enum(getattr(annotation, "spoof", "UNKNOWN")),
        "medical": _safe_enum(getattr(annotation, "medical", "UNKNOWN")),
        "violence": _safe_enum(getattr(annotation, "violence", "UNKNOWN")),
        "racy": _safe_enum(getattr(annotation, "racy", "UNKNOWN")),
    }
