import os
from google.cloud import firestore
import json

def persist_expense_record(record_id: str, record_data: dict, collection_name: str = "expense_records") -> None:
    """
    Persists normalized expense records in a Google Cloud Firestore managed document store.
    
    Args:
        record_id: A unique identifier for the expense record.
        record_data: The normalized expense record data (dictionary).
        collection_name: The name of the Firestore collection to store records in.
    """
    # Initialize Firestore DB client
    # The client automatically uses GOOGLE_APPLICATION_CREDENTIALS or other standard auth.
    db = firestore.Client()

    # Get a reference to the collection and document
    doc_ref = db.collection(collection_name).document(record_id)

    try:
        doc_ref.set(record_data)
        print(f"Successfully persisted record '{record_id}' to Firestore collection '{collection_name}'.")
    except Exception as e:
        print(f"Error persisting record '{record_id}' to Firestore: {e}")

def retrieve_expense_record(record_id: str, collection_name: str = "expense_records") -> dict | None:
    """
    Retrieves an expense record from Firestore.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(record_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Successfully retrieved record '{record_id}' from Firestore.")
        return doc.to_dict()
    else:
        print(f"Record '{record_id}' not found in Firestore.")
        return None

if __name__ == '__main__':
    # Example Usage
    sample_expense_record = {
        "document_type": "invoice",
        "vendor_name": "Cloud Services Corp.",
        "transaction_date": "2023-10-27",
        "total_amount": 500.25,
        "currency": "USD",
        "line_items": [
            {"description": "Compute usage", "amount": 450.00},
            {"description": "Storage", "amount": 50.25}
        ],
        "tax_amount": 0.0,
        "notes": "Monthly cloud bill."
    }

    record_unique_id = "invoice_20231027_001"

    # To run this example, ensure you have Google Cloud authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # and Firestore enabled for your project.
    print(f"Attempting to persist record '{record_unique_id}'...")
    persist_expense_record(record_unique_id, sample_expense_record)

    print(f"\nAttempting to retrieve record '{record_unique_id}'...")
    retrieved_record = retrieve_expense_record(record_unique_id)
    if retrieved_record:
        print("Retrieved Record:", json.dumps(retrieved_record, indent=2))

    print("\nAttempting to retrieve a non-existent record...")
    non_existent_record = retrieve_expense_record("non_existent_id")
