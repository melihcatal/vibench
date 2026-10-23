import os
import json
from google.cloud import firestore


def persist_expense_record(
    expense_record: dict, collection_name: str = "expense_records"
) -> str:
    """
    Persists normalized expense records in Google Firestore.
    The GOOGLE_APPLICATION_CREDENTIALS environment variable must be set or authentication configured.
    """
    # Initialize Firestore client. Project ID is usually picked up from GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client()

    try:
        # Add a new document to the specified collection
        doc_ref = db.collection(collection_name).add(expense_record)
        record_id = doc_ref[
            1
        ].id  # doc_ref is a tuple: (update_time, DocumentReference)
        print(f"Expense record successfully stored with ID: {record_id}")
        return record_id
    except Exception as e:
        print(f"Error persisting expense record to Firestore: {e}")
        raise


if __name__ == "__main__":
    # Example usage - ensure GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT is set
    google_cloud_project = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not google_cloud_project:
        print(
            "Please ensure GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT environment variable is set for Google Firestore."
        )
    else:
        dummy_normalized_expense = {
            "transaction_type": "expense",
            "vendor": {"name": "Example Vendor Inc.", "address": "123 Vendor Lane"},
            "date": "2023-11-15",
            "total_amount": {"value": 99.99, "currency": "USD"},
            "tax_amount": {"value": 5.00, "currency": "USD"},
            "line_items": [
                {
                    "description": "Service Fee",
                    "quantity": 1,
                    "unit_price": 99.99,
                    "total": 99.99,
                }
            ],
            "document_type": "invoice",
            "raw_extraction": {
                "source": "DocumentAI",
                "data": {"some_raw_field": "value"},
            },
            "validation_results": {"status": "success", "issues": []},
        }

        print(f"Persisting normalized expense record to Google Firestore...")
        # try:
        #     persisted_id = persist_expense_record(dummy_normalized_expense)
        #     print(f"Persisted record ID: {persisted_id}")
        # except Exception as e:
        #     print(f"Failed to persist record: {e}")
