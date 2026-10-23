from google.cloud import firestore

from database_client import document_ref
from database_models import normalize_document_id, normalize_payload, UpdateResult


def conditional_update(document_id, expected_version, updates):
    document_id = normalize_document_id(document_id)
    updates = normalize_payload(updates)
    ref = document_ref(document_id)
    transaction = firestore.Transaction()

    @firestore.transactional
    def _run(txn):
        snapshot = ref.get(transaction=txn)
        if not snapshot.exists:
            return UpdateResult(id=document_id, data={}, updated=False)
        current = snapshot.to_dict() or {}
        if expected_version is not None and current.get("version") != expected_version:
            return UpdateResult(id=document_id, data=current, updated=False)
        current.update(updates)
        if expected_version is not None:
            current["version"] = expected_version + 1
        txn.set(ref, current, merge=False)
        return UpdateResult(id=document_id, data=current, updated=True)

    return _run(transaction)
