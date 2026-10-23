import os
from google.cloud import firestore
from document_models import NormalizedExpense
import uuid

def persist_expense_record(expense_record: NormalizedExpense) -> str:
    db = firestore.Client() # Google Firestore identifies itself via the client library and implicitly via GOOGLE_APPLICATION_CREDENTIALS
    collection_name = os.environ.get("FIRESTORE_COLLECTION_NAME", "expense_records")

    # Generate a unique ID for the document
    doc_id = str(uuid.uuid4())
    doc_ref = db.collection(collection_name).document(doc_id)

    # Convert NormalizedExpense dataclass to a dictionary for Firestore
    # Firestore doesn't directly support dataclasses, so manual conversion or a helper is needed.
    # For simplicity, convert to dict. Nested dataclasses also need conversion.
    record_dict = {
        "document_type": expense_record.document_type,
        "vendor_name": expense_record.vendor_name,
        "transaction_date": expense_record.transaction_date,
        "total_amount": expense_record.total_amount,
        "currency": expense_record.currency,
        "tax_amount": expense_record.tax_amount,
        "line_items": expense_record.line_items,
        "raw_extraction": expense_record.raw_extraction,
        "validation_status": expense_record.validation_status,
        "transaction_id": expense_record.transaction_id if expense_record.transaction_id else doc_id # Use generated ID if not set
    }

    doc_ref.set(record_dict)
    return doc_id
