import os
from database_client import get_firestore_client
from database_models import Document


def query_documents(collection_name: str, field_name: str, field_value: str):
    """
    Queries documents by a field value in Google Cloud Firestore.
    """
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    results = [Document.from_dict(doc.id, doc.to_dict()) for doc in docs]
    return results
