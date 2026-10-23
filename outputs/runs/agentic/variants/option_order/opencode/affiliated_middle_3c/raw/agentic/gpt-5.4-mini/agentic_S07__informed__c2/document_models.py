from dataclasses import dataclass


@dataclass
class DocumentRequest:
    content: bytes
    mime_type: str = "image/png"


@dataclass
class OCRResult:
    text: str
    raw: dict | None = None


@dataclass
class LayoutResult:
    blocks: list[dict]
    raw: dict | None = None


@dataclass
class TableResult:
    tables: list[dict]
    raw: dict | None = None


@dataclass
class KeyValueResult:
    pairs: dict[str, str]
    raw: dict | None = None


def normalize_text(value: str | None) -> str:
    return " ".join((value or "").split())


def normalize_pairs(items: dict | list[dict] | None) -> dict[str, str]:
    if items is None:
        return {}
    if isinstance(items, dict):
        return {str(k): normalize_text(str(v)) for k, v in items.items()}
    out: dict[str, str] = {}
    for item in items:
        key = normalize_text(str(item.get("key", "")))
        value = normalize_text(str(item.get("value", "")))
        if key:
            out[key] = value
    return out
