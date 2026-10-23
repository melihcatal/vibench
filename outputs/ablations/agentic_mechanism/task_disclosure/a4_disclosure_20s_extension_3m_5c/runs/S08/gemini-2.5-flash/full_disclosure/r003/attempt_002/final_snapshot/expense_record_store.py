from google.cloud import firestore

def get_firestore_client():
    """Initializes and returns a Firestore client."""
    return firestore.Client()

def save_expense_record(record: dict, collection_name: str = "expense_records"):
    """
    Saves a normalized expense record to a Firestore collection.

    Args:
        record: The normalized expense record as a dictionary.
        collection_name: The name of the Firestore collection to save the record to.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).add(record)
    return doc_ref