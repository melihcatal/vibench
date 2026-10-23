from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_url: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/png"
    prompt: str = ""


@dataclass
class VisionResult:
    text: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    if isinstance(value, dict):
        for key in ("text", "content", "description", "labels", "response"):
            if key in value:
                normalized = normalize_text(value[key])
                if normalized:
                    return normalized
    return str(value).strip()


def extract_items(text: str) -> List[str]:
    items = []
    for line in text.splitlines():
        cleaned = line.strip().lstrip("-•*").strip()
        if cleaned:
            items.append(cleaned)
    return items


def normalize_response(raw: Any) -> VisionResult:
    text = normalize_text(raw)
    return VisionResult(text=text, raw=raw)
