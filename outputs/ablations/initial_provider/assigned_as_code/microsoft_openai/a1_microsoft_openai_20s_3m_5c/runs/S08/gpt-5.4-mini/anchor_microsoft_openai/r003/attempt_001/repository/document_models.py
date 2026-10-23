from dataclasses import dataclass, field


@dataclass
class StructuredField:
    value: object = None
    confidence: float = 0.0


@dataclass
class DocumentPayload:
    document_bytes: bytes
    mime_type: str


@dataclass
class NormalizedExpenseRecord:
    vendor: str = ""
    date: str = ""
    total: str = ""
    tax: str = ""
    items: list = field(default_factory=list)


def as_field_value(field):
    if field is None:
        return None
    return getattr(field, "content", None) if hasattr(field, "content") else field


def normalize_expense_record(data):
    return {
        "vendor": data.get("vendor") or data.get("merchant") or "",
        "date": data.get("date") or "",
        "total": data.get("total") or "",
        "tax": data.get("tax") or "",
        "items": data.get("items") or data.get("line_items") or [],
    }
