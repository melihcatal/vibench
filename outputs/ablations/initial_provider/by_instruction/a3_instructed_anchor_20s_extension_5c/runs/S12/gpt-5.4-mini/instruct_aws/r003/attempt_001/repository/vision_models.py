from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ImageInput:
    image_path: str

    def as_path(self) -> Path:
        return Path(self.image_path)


@dataclass
class VisionResult:
    provider: str
    kind: str
    image_path: str
    content: Any
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


def normalize_labels(labels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in labels:
        normalized.append({"name": str(item.get("name", "")), "confidence": float(item.get("confidence", 0.0))})
    return normalized


def normalize_text_lines(lines: List[str]) -> List[str]:
    return [line.strip() for line in lines if line and line.strip()]
