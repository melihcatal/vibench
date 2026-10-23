from google.cloud import firestore
import os

def fetch_document(collection_name: str, document_id: str):
    """Fetches a document by identifier from Firestore."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "document": doc.to_dict()}
    else:
        return {"status": "not_found"}
