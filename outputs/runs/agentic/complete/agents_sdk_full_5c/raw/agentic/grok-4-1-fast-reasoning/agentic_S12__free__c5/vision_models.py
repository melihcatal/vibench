from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class ImageLabels:
    labels: List[dict[str, Any]] = field(default_factory=list)

@dataclass
class ImageText:
    texts: List[str] = field(default_factory=list)

@dataclass
class ImageSafety:
    adult: str = ""
    racy: str = ""
    violence: str = ""
    medical: str = ""

def parse_labels(annotations) -> ImageLabels:
    if not annotations:
        return ImageLabels()
    return ImageLabels(labels=[
        {"description": ann.description, "score": ann.score}
        for ann in annotations
    ])

def parse_safety_annotation(annotation) -> ImageSafety:
    if not annotation:
        return ImageSafety()
    return ImageSafety(
        adult=annotation.adult.name if hasattr(annotation.adult, 'name') else "",
        racy=annotation.racy.name if hasattr(annotation.racy, 'name') else "",
        violence=annotation.violence.name if hasattr(annotation.violence, 'name') else "",
        medical=annotation.medical.name if hasattr(annotation.medical, 'name') else "",
    )