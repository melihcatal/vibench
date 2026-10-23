from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


def _read_image_input(image_input: Any) -> bytes:
    if isinstance(image_input, bytes):
        return image_input
    if isinstance(image_input, str):
        p = Path(image_input)
        if p.exists():
            return p.read_bytes()
        return image_input.encode("utf-8")
    if hasattr(image_input, "read"):
        data = image_input.read()
        return data if isinstance(data, bytes) else str(data).encode("utf-8")
    raise TypeError("Unsupported image input type")


@dataclass
class OCRRequest:
    image: Any
    locale: Optional[str] = None

    def to_bytes(self) -> bytes:
        return _read_image_input(self.image)


@dataclass
class OCRResponse:
    text: str
    raw: Dict[str, Any]


def normalize_text(text: Optional[str]) -> str:
    return " ".join((text or "").split())


def normalize_lines(lines: List[str]) -> List[str]:
    return [normalize_text(line) for line in lines if normalize_text(line)]


def normalize_kv_pairs(items: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    normalized = []
    for item in items:
        normalized.append(
            {
                "key": normalize_text(item.get("key")),
                "value": normalize_text(item.get("value")),
            }
        )
    return normalized
