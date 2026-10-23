from dataclasses import dataclass
from typing import Any


@dataclass
class OCRDocumentRequest:
    document_url: str


@dataclass
class OCRDocumentResponse:
    text: str
    raw: Any | None = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    if isinstance(value, dict):
        parts = []
        for key in ("content", "text", "value", "lines"):
            if key in value:
                text = normalize_text(value[key])
                if text:
                    parts.append(text)
        return "\n".join(parts)
    return str(value).strip()


def as_response(text: Any, raw: Any | None = None) -> OCRDocumentResponse:
    return OCRDocumentResponse(text=normalize_text(text), raw=raw)
