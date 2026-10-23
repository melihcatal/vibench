from google.cloud import firestore

from database_client import get_collection
from database_models import ConditionalUpdateRequest


def conditional_update(request: ConditionalUpdateRequest):
    client = get_collection(request.collection).database.client
    ref = get_collection(request.collection).document(request.document_id)

    @firestore.transactional
    def _run(transaction):
        snapshot = ref.get(transaction=transaction)
        if not snapshot.exists:
            return None
        current = snapshot.to_dict() or {}
        if request.expected_version is not None and current.get("version") != request.expected_version:
            return None
        updated = dict(current)
        updated.update(request.updates)
        if request.expected_version is not None:
            updated["version"] = request.expected_version + 1
        transaction.set(ref, updated, merge=True)
        return updated

    transaction = client.transaction()
    return _run(transaction)
