from dataclasses import dataclass


@dataclass
class StructuredDocumentRequest:
    document_bytes: bytes


@dataclass
class StructuredDocumentResponse:
    fields: dict
    confidence: dict


def normalize_fields(fields):
    return {k: v for k, v in (fields or {}).items() if v is not None}


def build_standard_expense_schema(data):
    return {
        "vendor": data.get("vendor", ""),
        "date": data.get("date", ""),
        "total": data.get("total", ""),
        "tax": data.get("tax", ""),
        "items": data.get("items", []),
        "notes": data.get("notes", ""),
        "currency": data.get("currency", ""),
    }
