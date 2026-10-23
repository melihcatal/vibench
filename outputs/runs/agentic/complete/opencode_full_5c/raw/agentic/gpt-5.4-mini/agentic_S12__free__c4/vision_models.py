from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class VisionLabelsRequest:
    image: Any


@dataclass
class VisionDescriptionRequest:
    image: Any


@dataclass
class VisionTextRequest:
    image: Any


@dataclass
class VisionSafetyRequest:
    image: Any


@dataclass
class VisionResult:
    text: str
    raw: Optional[Dict[str, Any]] = None


def normalize_text(text: Any) -> str:
    if isinstance(text, str):
        return text.strip()
    if isinstance(text, list):
        return " ".join(str(part).strip() for part in text if str(part).strip())
    return str(text).strip()


def normalize_labels(text: str) -> List[str]:
    parts = [p.strip() for p in text.replace("\n", ",").split(",")]
    return [p for p in parts if p]


def result_from_response(
    text: str, raw: Optional[Dict[str, Any]] = None
) -> VisionResult:
    return VisionResult(text=normalize_text(text), raw=raw)


def to_dict(instance: Any) -> Dict[str, Any]:
    return asdict(instance)
