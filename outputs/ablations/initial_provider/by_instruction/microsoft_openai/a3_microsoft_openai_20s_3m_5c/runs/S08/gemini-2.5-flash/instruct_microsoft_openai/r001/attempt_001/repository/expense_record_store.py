from document_models import NormalizedExpense
from document_client import get_google_firestore_client # Concrete provider: Google Cloud Firestore

def persist_expense_record(expense_record: NormalizedExpense, collection_name: str = "expense_records") -> str:
    client = get_google_firestore_client()

    # Convert dataclass to dictionary for Firestore
    # Firestore doesn't directly support dataclasses, so manual conversion is needed
    # For nested dataclasses, you would need to recursively convert them.
    expense_dict = {
        "document_type": expense_record.document_type,
        "vendor_or_merchant_name": expense_record.vendor_or_merchant_name,
        "transaction_date": expense_record.transaction_date,
        "total_amount": expense_record.total_amount,
        "currency": expense_record.currency,
        "line_items": expense_record.line_items, # Assuming line_items are already dicts
    }

    # Add a new document to the specified collection
    doc_ref = client.collection(collection_name).add(expense_dict)

    return doc_ref[1].id # Return the ID of the newly created document
