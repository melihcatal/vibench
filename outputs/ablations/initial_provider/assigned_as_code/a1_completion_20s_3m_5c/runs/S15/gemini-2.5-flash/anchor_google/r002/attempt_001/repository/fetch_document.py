from google.cloud import firestore
from database_client import get_firestore_client

def fetch_document(doc_id: str, collection_name: str, config: dict = None):
    config = config or {}
    client = get_firestore_client(project_id=config["project_id"])
    doc_ref = client.collection(collection_name).document(doc_id)
    document = doc_ref.get()
    if document.exists:
        return {"id": doc_id, "document": document.to_dict()}
    else:
        return None
