import os
from database_client import get_firestore_client
from database_models import Document


def query_documents(collection_name: str, field_name: str, field_value: Any):
    """Queries documents by a field value from Google Firestore.

    Args:
        collection_name (str): The name of the Firestore collection.
        field_name (str): The name of the field to query by.
        field_value (Any): The value of the field to match.

    Returns:
        list[Document]: A list of matching document objects.
    """
    db = get_firestore_client()
    query = db.collection(collection_name).where(field_name, "==", field_value)
    results = query.stream()

    documents = []
    for doc in results:
        documents.append(Document.from_firestore(doc.id, doc.to_dict()))
    return documents
