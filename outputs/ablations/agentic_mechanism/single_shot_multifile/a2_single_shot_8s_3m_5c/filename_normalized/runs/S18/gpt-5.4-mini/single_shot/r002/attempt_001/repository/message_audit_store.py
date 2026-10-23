import os
from google.cloud import firestore
from messaging_models import success_result


def message_audit_store(record, collection_name=None):
    client = firestore.Client()
    collection = collection_name or os.getenv("FIRESTORE_AUDIT_COLLECTION", "message_audit")
    doc_ref = client.collection(collection).document()
    doc_ref.set(dict(record or {}))
    return success_result(provider="google_cloud_firestore", operation="message_audit_store", document_id=doc_ref.id, collection=collection)