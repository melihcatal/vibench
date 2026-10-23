from typing import Any, Dict

from document_models import DocumentExtractionResponse, normalize_confidence


def normalize_expense(extraction: DocumentExtractionResponse) -> Dict[str, Any]:
    fields = extraction.fields
    return {
        "source_provider": extraction.provider,
        "merchant_or_vendor": fields.get("merchant") or fields.get("vendor"),
        "transaction_date": fields.get("date"),
        "total_amount": fields.get("total"),
        "tax_amount": fields.get("tax"),
        "items": fields.get("items") or fields.get("line_items") or [],
        "confidence": normalize_confidence(fields.get("confidence", 0.0)),
    }
