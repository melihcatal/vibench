from google.cloud import firestore

def query_documents_by_field(project_id: str, collection_name: str, field_name: str, field_value: any):
    """Queries documents in a Firestore collection by a specific field value."""
    db = firestore.Client(project=project_id)
    collection_ref = db.collection(collection_name)
    query = collection_ref.where(field_name, "==", field_value)
    results = query.stream()
    return [doc.to_dict() for doc in results]

def query_documents_by_partition_key(project_id: str, collection_name: str, document_id: str):
    """Retrieves a single document by its document ID (partition-style key)."""
    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

