from dataclasses import dataclass


def normalize_entity(entity):
    name = getattr(entity, "description", None) or getattr(entity, "name", None) or ""
    score = float(getattr(entity, "score", 0.0) or 0.0)
    return {"name": name, "score": score}


def normalize_text_annotation(annotation):
    return {
        "text": getattr(annotation, "description", "") or "",
        "language": getattr(annotation, "locale", "") or "",
    }


@dataclass
class ImageAnalysisResult:
    items: list
