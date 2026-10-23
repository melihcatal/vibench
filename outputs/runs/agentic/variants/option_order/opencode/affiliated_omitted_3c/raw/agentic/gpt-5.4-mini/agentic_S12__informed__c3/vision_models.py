from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageInput:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/jpeg"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionResult:
    labels: List[str] = field(default_factory=list)
    description: str = ""
    text: List[str] = field(default_factory=list)
    safety: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


def normalize_strings(values: Any) -> List[str]:
    if values is None:
        return []
    if isinstance(values, str):
        return [values.strip()] if values.strip() else []
    out = []
    for value in values:
        text = str(value).strip()
        if text:
            out.append(text)
    return out
