from dataclasses import dataclass, asdict


@dataclass
class ExtractedField:
    name: str
    value: str | float | int | None
    confidence: float | None = None


@dataclass
class StructuredDocumentResponse:
    document_type: str
    fields: dict
    raw: dict | None = None


def normalize_money(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace(",", "").strip()
    return float(text)


def response_to_dict(response):
    return asdict(response)
