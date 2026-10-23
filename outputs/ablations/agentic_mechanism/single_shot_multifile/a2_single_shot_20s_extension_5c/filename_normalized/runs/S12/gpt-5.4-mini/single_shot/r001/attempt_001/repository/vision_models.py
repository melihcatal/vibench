from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Sequence


@dataclass
class ImageLabelDetectionRequest:
    image_path: str
    max_labels: int = 10
    language: str = "en"


@dataclass
class ImageLabel:
    name: str
    confidence: float


@dataclass
class ImageLabelDetectionResponse:
    labels: List[ImageLabel]
    raw: Dict[str, Any]

    def model_dump(self) -> Dict[str, Any]:
        return {"labels": [asdict(label) for label in self.labels], "raw": self.raw}


@dataclass
class ImageDescriptionRequest:
    image_path: str
    max_sentences: int = 2


@dataclass
class ImageDescriptionResponse:
    description: str
    confidence: float
    raw: Dict[str, Any]

    def model_dump(self) -> Dict[str, Any]:
        return {"description": self.description, "confidence": self.confidence, "raw": self.raw}


@dataclass
class ImageTextDetectionRequest:
    image_path: str
    language: str = "en"


@dataclass
class ImageTextDetectionResponse:
    text_lines: List[str]
    raw: Dict[str, Any]

    def model_dump(self) -> Dict[str, Any]:
        return {"text_lines": self.text_lines, "raw": self.raw}


@dataclass
class ImageSafetyRequest:
    image_path: str


@dataclass
class ImageSafetyResponse:
    safe: bool
    unsafe_score: float
    reasons: List[str]
    raw: Dict[str, Any]

    def model_dump(self) -> Dict[str, Any]:
        return {"safe": self.safe, "unsafe_score": self.unsafe_score, "reasons": self.reasons, "raw": self.raw}


def normalize_label_items(items: Sequence[Dict[str, Any]], max_items: int = 10) -> List[ImageLabel]:
    labels: List[ImageLabel] = []
    for item in items[:max_items]:
        name = str(item.get("name", "")).strip()
        confidence = float(item.get("confidence", 0.0) or 0.0)
        if name:
            labels.append(ImageLabel(name=name, confidence=confidence))
    return labels


def normalize_text_lines(blocks: Sequence[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    for block in blocks:
        for line in block.get("lines", []):
            text = str(line.get("text", "")).strip()
            if text:
                lines.append(text)
    return lines
