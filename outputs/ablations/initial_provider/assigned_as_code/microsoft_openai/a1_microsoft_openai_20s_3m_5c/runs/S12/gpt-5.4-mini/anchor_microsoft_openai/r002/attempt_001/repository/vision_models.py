from dataclasses import dataclass
from typing import Any, Dict, Optional


def get_image_bytes(payload: Dict[str, Any]) -> bytes:
    value = payload.get('image_bytes')
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    raise ValueError('payload.image_bytes is required')


def normalize_text(value: Any) -> str:
    if value is None:
        return ''
    return str(value).strip()


def make_config(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return dict(config or {})


@dataclass
class VisionTextResult:
    text: str
    confidence: Optional[float] = None


@dataclass
class VisionSummaryResult:
    summary: str
