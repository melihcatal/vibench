from database_client import collection_ref, get_firestore_client, serialize_snapshot
from database_models import DocumentFetchRequest


def fetch_document(request: DocumentFetchRequest):
    db = get_firestore_client()
    snapshot = collection_ref(db, request.collection).document(request.document_id).get()
    return serialize_snapshot(snapshot)
