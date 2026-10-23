from google.cloud import firestore

def fetch_document(collection_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its identifier from a Google Cloud Firestore collection.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to fetch.

    Returns:
        A dictionary representing the document data if found, otherwise None.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None
