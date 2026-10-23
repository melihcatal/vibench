import os
import json
from google.cloud import firestore


def store_expense_record(record: dict, collection_name: str = "expenses") -> str:
    """Persist a normalized expense record to Google Firestore.

    Expected keys in `record` follow the normalized schema:
      - vendor (str)
      - date (str, YYYY-MM-DD)
      - total (float)
      - items (list of dicts with description, quantity, unit_price, total)

    Returns the auto‑generated document ID.
    """
    # Load Firestore credentials from env var (default client uses Application Default Credentials)
    db = firestore.Client()
    collection = db.collection(collection_name)
    doc_ref = collection.document()  # auto-id
    doc_ref.set(record)
    doc_id = doc_ref.id
    print(f"Stored expense record {doc_id} in collection '{collection_name}'.")
    return doc_id


# Minimal command‑line demo
if __name__ == "__main__":
    sample_record = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 125.50,
        "items": [
            {
                "description": "Widget A",
                "quantity": 2,
                "unit_price": 45.00,
                "total": 90.00,
            },
            {
                "description": "Widget B",
                "quantity": 1,
                "unit_price": 35.50,
                "total": 35.50,
            },
        ],
    }
    # Ensure Google Application Credentials env var is set in your environment
    doc_id = store_expense_record(sample_record)
    print("Document ID:", doc_id)
