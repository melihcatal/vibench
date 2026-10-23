import os
from database_client import get_firestore_client
from database_models import Document


def upsert_document(collection_name: str, document_id: str, document_data: dict):
    """Upserts a JSON document into Google Firestore by its primary identifier.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to upsert.
        document_data (dict): The data of the document to upsert.

    Returns:
        dict: A dictionary containing the updated document ID.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(document_data)
    return {"document_id": document_id}
