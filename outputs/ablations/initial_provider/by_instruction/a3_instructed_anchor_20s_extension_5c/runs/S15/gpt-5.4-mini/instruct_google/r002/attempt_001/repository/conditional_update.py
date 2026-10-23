from google.cloud import firestore

from database_client import collection_ref, get_firestore_client, serialize_snapshot
from database_models import DocumentConditionalUpdateRequest


def conditional_update(request: DocumentConditionalUpdateRequest):
    db = get_firestore_client()
    ref = collection_ref(db, request.collection).document(request.document_id)
    transaction = db.transaction()

    @firestore.transactional
    def apply(txn):
        snapshot = ref.get(transaction=txn)
        if not snapshot.exists:
            return {}
        if request.etag is not None and snapshot.get("etag") != request.etag:
            return {}
        txn.update(ref, request.updates)
        return serialize_snapshot(ref.get(transaction=txn))

    return apply(transaction)
