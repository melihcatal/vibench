
from google.cloud import firestore

def query_documents_by_field(collection_name: str, field_name: str, field_value: str):
    """Queries documents in a Firestore collection by a specific field value."""
    db = firestore.Client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    return [doc.to_dict() for doc in docs]

def query_documents_by_partition_key(collection_path: str):
    """Queries documents within a specific collection path, simulating a partition key."""
    db = firestore.Client()
    docs = db.collection(collection_path).stream()
    return [doc.to_dict() for doc in docs]

