from database_client import collection_ref, get_firestore_client, serialize_snapshot
from database_models import DocumentQueryRequest


def query_documents(request: DocumentQueryRequest):
    db = get_firestore_client()
    docs = collection_ref(db, request.collection).where(request.field_name, "==", request.field_value).stream()
    return [serialize_snapshot(doc) for doc in docs]
