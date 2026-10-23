
from google.cloud import firestore
import os
from document_client import GoogleFirestoreManager
from document_models import ExpenseRecord

def persist_expense_record(expense_record: ExpenseRecord) -> str:
    """
    Persists normalized expense records in Google Cloud Firestore.
    Returns the ID of the stored document.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    collection_name = os.getenv("FIRESTORE_COLLECTION_NAME", "expense_records")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    firestore_manager = GoogleFirestoreManager(project_id)
    db = firestore_manager.get_firestore_client()

    # Convert Pydantic model to dict for Firestore
    record_dict = expense_record.model_dump(mode='json', exclude_none=True)

    try:
        # Add a new document to the collection
        doc_ref = db.collection(collection_name).add(record_dict)
        doc_id = doc_ref[1].id # doc_ref is a tuple (timestamp, document_reference)
        print(f"Expense record stored with ID: {doc_id}")
        return doc_id
    except Exception as e:
        print(f"Error storing expense record in Firestore: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    expense_to_store = ExpenseRecord(
        document_type="receipt",
        vendor_name="Cafe Connect",
        transaction_date="2023-10-27",
        total_amount=15.75,
        currency="EUR",
        line_items=[
            {"description": "Espresso", "amount": 3.50, "quantity": 1},
            {"description": "Sandwich", "amount": 12.25, "quantity": 1}
        ],
        notes="Quick lunch meeting."
    )

    # Ensure GCP_PROJECT_ID is set as an environment variable
    # For local testing, you might need to authenticate with `gcloud auth application-default login`
    # try:
    #     stored_id = persist_expense_record(expense_to_store)
    #     print(f"Successfully stored expense with ID: {stored_id}")
    # except Exception as e:
    #     print(f"Failed to store expense: {e}")
    pass
