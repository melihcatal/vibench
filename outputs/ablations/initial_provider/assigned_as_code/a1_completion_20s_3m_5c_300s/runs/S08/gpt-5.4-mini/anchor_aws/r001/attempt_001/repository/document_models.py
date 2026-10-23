from dataclasses import dataclass, field


@dataclass
class DocumentRequest:
    document_bytes: bytes = b""
    config: dict = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    vendor: str = ""
    date: str = ""
    total: str = ""
    currency: str = ""
    notes: str = ""
    items: list = field(default_factory=list)


def normalize_field_text(value):
    if value is None:
        return ""
    return str(value).strip()


def build_expense_schema(record):
    return {
        "vendor": normalize_field_text(record.get("vendor")),
        "date": normalize_field_text(record.get("date")),
        "total": normalize_field_text(record.get("total")),
        "currency": normalize_field_text(record.get("currency")),
        "notes": normalize_field_text(record.get("notes")),
        "items": record.get("items", []),
    }
