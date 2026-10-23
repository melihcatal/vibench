from dataclasses import dataclass


@dataclass
class DocumentExtractionRequest:
    document_bytes: bytes
    mime_type: str = "application/pdf"


@dataclass
class DocumentExtractionResponse:
    fields: dict
    confidence: float | None = None


def normalize_number(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace(",", "").strip()
    try:
        return float(text)
    except ValueError:
        return None


def standardize_expense_record(payload: dict) -> dict:
    return {
        "vendor": payload.get("vendor") or payload.get("merchant"),
        "date": payload.get("date"),
        "total": normalize_number(payload.get("total")),
        "tax": normalize_number(payload.get("tax")),
        "items": payload.get("items") or payload.get("line_items") or [],
        "source": payload.get("source", "textract"),
    }
