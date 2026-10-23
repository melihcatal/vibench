from __future__ import annotations

from typing import Any, Dict

from document_models import StructuredDocumentResponse, normalize_currency_amount

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"


def normalize_expense_fields(extracted: StructuredDocumentResponse) -> Dict[str, Any]:
    fields = extracted.fields
    return {
        "source": "azure-ai-documentintelligence:prebuilt-invoice",
        "vendor": fields.get("vendor_name", {}).value if "vendor_name" in fields else None,
        "date": fields.get("invoice_receipt_date", {}).value if "invoice_receipt_date" in fields else None,
        "total": normalize_currency_amount(fields.get("total", {}).value if "total" in fields else None),
        "tax": normalize_currency_amount(fields.get("tax", {}).value if "tax" in fields else None),
        "items": fields.get("items", {}).value if "items" in fields else [],
    }
