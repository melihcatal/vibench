from document_models import StructuredDocumentResponse


def normalize_expense(extracted):
    if isinstance(extracted, StructuredDocumentResponse):
        extracted = extracted.raw
    return {
        "merchant": extracted.get("merchant") or extracted.get("vendor"),
        "date": extracted.get("date"),
        "total": extracted.get("total"),
        "tax": extracted.get("tax"),
        "items": extracted.get("items") or extracted.get("line_items") or [],
    }
