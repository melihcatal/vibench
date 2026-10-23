from typing import Dict, Any
from document_models import ExtractedDocument, NormalizedExpense

def normalize_expense(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    document_type = extracted_data.get("document_type")
    extracted_doc = None
    if document_type == "invoice":
        if "invoices" in extracted_data and extracted_data["invoices"]:
            invoice_data = extracted_data["invoices"][0]
            extracted_doc = ExtractedDocument(**invoice_data)
    elif document_type == "receipt":
        if "receipt" in extracted_data:
            receipt_data = extracted_data["receipt"]
            extracted_doc = ExtractedDocument(**receipt_data)

    if not extracted_doc:
        raise ValueError("No extracted document found for normalization.")

    normalized_expense = NormalizedExpense(
        document_type=document_type,
        vendor_name=extracted_doc.vendor or extracted_doc.merchant,
        transaction_date=extracted_doc.date,
        total_amount=float(extracted_doc.total) if extracted_doc.total else None,
        tax_amount=float(extracted_doc.tax) if extracted_doc.tax else None,
        currency="USD", # Assuming USD for now, can be extracted later
        line_items=[item.dict() for item in (extracted_doc.line_items or extracted_doc.items)],
    )

    return {"normalized_expense": normalized_expense.dict()}
