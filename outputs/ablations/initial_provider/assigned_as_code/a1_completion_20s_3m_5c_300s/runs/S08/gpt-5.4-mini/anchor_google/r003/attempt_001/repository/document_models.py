from dataclasses import dataclass


def normalize_text(value):
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def normalize_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


@dataclass
class DocumentRequest:
    document_bytes: bytes
    mime_type: str
    locale: str = "en"


@dataclass
class DocumentResponse:
    data: dict
