from database_client import get_firestore_client

def fetch_document(collection_name: str, document_id: str) -> dict | None:
    """Fetches a document by its ID from a Google Cloud Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to fetch.

    Returns:
        dict | None: The document data if found, otherwise None.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        print(f"Document {document_id} fetched successfully from collection {collection_name}.")
        return doc.to_dict()
    else:
        print(f"Document {document_id} not found in collection {collection_name}.")
        return None
