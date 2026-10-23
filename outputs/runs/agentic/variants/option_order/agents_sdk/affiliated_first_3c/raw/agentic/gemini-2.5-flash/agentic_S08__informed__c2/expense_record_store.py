import os
from google.cloud import firestore
from document_models import NormalizedExpense
import json

def get_firestore_client():
    """Returns a Google Cloud Firestore client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # The GOOGLE_CLOUD_PROJECT environment variable should also be set.
    return firestore.Client()

def persist_expense_record(expense_record: NormalizedExpense, collection_name: str = "expense_records") -> str:
    """
    Persists normalized expense records in Google Firestore.
    Returns the document ID of the stored record.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document()

    # Convert Pydantic model to a dictionary suitable for Firestore
    record_dict = expense_record.dict(by_alias=True, exclude_unset=True)

    try:
        doc_ref.set(record_dict)
        return doc_ref.id
    except Exception as e:
        print(f"Error persisting expense record to Firestore: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    #
    # from document_models import NormalizedExpense, LineItem
    #
    # example_expense = NormalizedExpense(
    #     document_type="receipt",
    #     merchant_name="Coffee Shop",
    #     transaction_date="2023-11-05",
    #     total_amount=4.75,
    #     currency="USD",
    #     tax_amount=0.30,
    #     line_items=[
    #         LineItem(description="Coffee", quantity=1, total_price=3.50),
    #         LineItem(description="Muffin", quantity=1, total_price=1.25)
    #     ],
    #     confidence_scores={
    #         "merchant_name": 0.98,
    #         "total_amount": 0.95
    #     }
    # )
    #
    # try:
    #     document_id = persist_expense_record(example_expense)
    #     print(f"Expense record persisted with ID: {document_id}")
    # except Exception as e:
    #     print(f"Failed to persist record: {e}")
    pass
