from document_client import get_google_firestore_client
from document_models import ExpenseDocument


def store_expense_record(expense_document: ExpenseDocument) -> str:
    db = get_google_firestore_client()

    doc_ref = db.collection("expense_records").document()

    expense_data = {
        "document_type": expense_document.document_type,
        "vendor_name": expense_document.vendor_name,
        "document_date": expense_document.document_date,
        "total_amount": expense_document.total_amount,
        "tax_amount": expense_document.tax_amount,
        "currency": expense_document.currency,
        "line_items": [item.__dict__ for item in expense_document.line_items],
        "merchant_name": expense_document.merchant_name,
        "notes": expense_document.notes,
        "validation_status": expense_document.validation_status,
        "raw_extraction_data": expense_document.raw_extraction_data,
    }

    doc_ref.set(expense_data)
    return doc_ref.id
