import os
from google.cloud import firestore
from typing import Dict, Any, Optional

def persist_expense_record(collection_name: str, expense_record: Dict[str, Any], document_id: Optional[str] = None) -> str:
    """
    Persists normalized expense records in Google Firestore.
    Returns the ID of the created or updated document.
    """
    # Initialize Firestore client
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set up
    db = firestore.Client()

    # Get a reference to the collection
    collection_ref = db.collection(collection_name)

    if document_id:
        # Update an existing document
        doc_ref = collection_ref.document(document_id)
        doc_ref.set(expense_record) # set() will create if it doesn't exist, or overwrite
        print(f"Document with ID '{document_id}' updated in collection '{collection_name}'.")
    else:
        # Add a new document with an auto-generated ID
        update_time, doc_ref = collection_ref.add(expense_record)
        document_id = doc_ref.id
        print(f"New document created with ID '{document_id}' in collection '{collection_name}'.")
    
    return document_id

if __name__ == "__main__":
    # Example normalized expense record
    example_expense_record = {
        "document_type": "invoice",
        "vendor_name": "Example Corp",
        "transaction_date": "2023-10-27T14:00:00",
        "total_amount": 250.00,
        "currency": "USD",
        "tax_amount": 15.00,
        "line_items": [
            {"description": "Consulting Fee", "quantity": 1, "unit_price": 235.00, "total": 235.00},
            {"description": "Sales Tax", "quantity": 1, "unit_price": 15.00, "total": 15.00}
        ],
        "raw_extraction": {},
        "validation_status": {"is_valid": True, "issues": []}
    }

    COLLECTION_NAME = "expense_records"

    # To run this example, ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # and your Google Cloud project has Firestore enabled.

    # Persist a new record
    # new_doc_id = persist_expense_record(COLLECTION_NAME, example_expense_record)
    # print(f"Persisted new record with ID: {new_doc_id}")

    # Example of updating an existing record (uncomment and replace with a real ID)
    # existing_doc_id = "replace_with_an_existing_firestore_doc_id"
    # updated_expense_record = example_expense_record.copy()
    # updated_expense_record["notes"] = "Updated this record with additional notes."
    # updated_doc_id = persist_expense_record(COLLECTION_NAME, updated_expense_record, existing_doc_id)
    # print(f"Updated record with ID: {updated_doc_id}")
