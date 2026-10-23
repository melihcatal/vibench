import os
from google.cloud import firestore
from document_models import NormalizedExpense

def persist_expense_record(expense_record: NormalizedExpense, collection_name: str = "expense_records") -> str:
    """
    Persists normalized expense records in a managed document store (Google Firestore).
    """
    # Google Cloud client libraries automatically use GOOGLE_APPLICATION_CREDENTIALS
    # or default service account if running on GCE/Cloud Functions/Run/etc.
    db = firestore.Client()

    # Convert NormalizedExpense dataclass to a dictionary for Firestore
    # The to_json method on NormalizedExpense (from document_models) also works for direct dict conversion
    # but we need to handle nested dataclasses correctly.
    record_dict = expense_record.__dict__.copy()
    record_dict["line_items"] = [item.__dict__ for item in expense_record.line_items]

    try:
        doc_ref = db.collection(collection_name).add(record_dict)
        print(f"Expense record successfully added with ID: {doc_ref[1].id}")
        return doc_ref[1].id
    except Exception as e:
        print(f"Error persisting expense record to Firestore: {e}")
        return ""

if __name__ == '__main__':
    # Example usage with a dummy NormalizedExpense object
    sample_expense = NormalizedExpense.from_dict({
        "expense_type": "receipt",
        "date": "2023-10-27",
        "merchant_name": "Local Cafe",
        "total_amount": 12.34,
        "currency": "USD",
        "tax_amount": 0.98,
        "line_items": [
            {"description": "Coffee", "quantity": 2, "unit_price": 4.50, "total_price": 9.00},
            {"description": "Pastry", "quantity": 1, "unit_price": 3.34, "total_price": 3.34}
        ],
        "original_extracted_data": {"receipt_image": "base64_encoded_image_data"}
    })

    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or gcloud auth application-default login has been run
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or gcloud is authenticated.")
        print("Also, make sure the project has Firestore enabled and permissions are granted.")
    else:
        print("Persisting sample expense record to Firestore...")
        record_id = persist_expense_record(sample_expense)
        if record_id:
            print(f"Record persisted successfully with ID: {record_id}")
        else:
            print("Failed to persist record.")
