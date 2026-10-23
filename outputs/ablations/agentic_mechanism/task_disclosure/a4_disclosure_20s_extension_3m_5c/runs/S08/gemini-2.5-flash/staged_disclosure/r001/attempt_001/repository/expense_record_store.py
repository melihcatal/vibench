from google.cloud import firestore

def get_firestore_client():
    """Initializes and returns a Firestore client."""
    return firestore.Client()

def add_expense_record(expense_record: dict, collection_name: str = 'expense_records'):
    """
    Persists a normalized expense record in Google Cloud Firestore.

    Args:
        expense_record (dict): A dictionary representing the normalized expense record.
        collection_name (str): The name of the Firestore collection to store records.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(expense_record)
    print(f"Expense record added with ID: {doc_ref.id}")

