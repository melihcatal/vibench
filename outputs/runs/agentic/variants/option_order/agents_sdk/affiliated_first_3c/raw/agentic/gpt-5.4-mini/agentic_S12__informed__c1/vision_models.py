from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ImageAnalysisResult:
    labels: List[str]
    description: str = ""
    text: List[str] = None
    unsafe: bool = False
    unsafe_reasons: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["text"] = data["text"] or []
        data["unsafe_reasons"] = data["unsafe_reasons"] or []
        return data


@dataclass
class ImageSummaryInput:
    labels: List[str]
    description: str
    detected_text: List[str]
    unsafe: bool = False


def normalize_strings(items: Optional[List[Any]]) -> List[str]:
    if not items:
        return []
    return [str(item).strip() for item in items if str(item).strip()]
