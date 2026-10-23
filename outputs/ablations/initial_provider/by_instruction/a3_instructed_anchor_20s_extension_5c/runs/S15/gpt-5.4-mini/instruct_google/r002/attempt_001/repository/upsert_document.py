from google.cloud import firestore

from database_client import collection_ref, get_firestore_client, serialize_snapshot
from database_models import DocumentUpsertRequest, document_key, normalize_document


def upsert_document(request: DocumentUpsertRequest):
    db = get_firestore_client()
    doc = normalize_document(request.document)
    doc_id = document_key(doc, request.key_field)
    ref = collection_ref(db, request.collection).document(doc_id)
    ref.set(doc, merge=True)
    return serialize_snapshot(ref.get())
