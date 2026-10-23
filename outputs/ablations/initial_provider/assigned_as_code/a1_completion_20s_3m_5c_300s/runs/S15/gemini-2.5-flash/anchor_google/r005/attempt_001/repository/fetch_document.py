from database_client import get_firestore_client
from database_models import Document
from google.cloud.firestore import Client


def fetch_document(document_id: str, collection_name: str, client: Client = None, project_id: str = None) -> Document or None:
    client = client or get_firestore_client(project_id=project_id)
    doc_ref = client.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return Document(id=doc.id, data=data)
    return None
