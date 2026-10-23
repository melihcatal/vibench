from database_client import get_firestore_client
from database_models import normalize_document_data

def upsert_document(collection_name: str, document_id: str, document_data: dict):
    """Upserts a JSON document into a Google Cloud Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to upsert.
        document_data (dict): The JSON document data to store.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    normalized_data = normalize_document_data(document_data)

    doc_ref.set(normalized_data)
    print(f"Document {document_id} upserted successfully in collection {collection_name}.")
