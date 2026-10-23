from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentRequest:
    content: bytes
    mime_type: str = "image/png"


@dataclass
class DocumentResponse:
    text: str = ""
    blocks: list[dict[str, Any]] = field(default_factory=list)
    tables: list[dict[str, Any]] = field(default_factory=list)
    key_values: dict[str, str] = field(default_factory=dict)


def normalize_text(text: str | None) -> str:
    return " ".join((text or "").split())


def normalize_pages(pages: list[Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for page in pages or []:
        items.append({"width": getattr(page, "width", None), "height": getattr(page, "height", None)})
    return items
