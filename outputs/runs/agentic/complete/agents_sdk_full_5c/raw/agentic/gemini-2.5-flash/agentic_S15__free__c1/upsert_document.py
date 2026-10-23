from google.cloud import firestore
import os

def upsert_document(collection_name: str, document_id: str, data: dict):
    """Upserts a JSON document by its primary identifier in Firestore."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    return {"status": "success", "document_id": document_id}
