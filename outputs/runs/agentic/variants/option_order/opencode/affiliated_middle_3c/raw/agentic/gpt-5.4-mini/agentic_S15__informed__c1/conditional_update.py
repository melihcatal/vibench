from google.cloud import firestore

from database_client import get_collection


def conditional_update(document_id: str, expected_version: int, updates: dict) -> dict:
    client = get_collection()._client
    doc_ref = get_collection().document(document_id)

    @firestore.transactional
    def _txn(transaction):
        snapshot = doc_ref.get(transaction=transaction)
        current_version = (
            int((snapshot.to_dict() or {}).get("version", 0)) if snapshot.exists else 0
        )
        if current_version != expected_version:
            return {
                "document_id": document_id,
                "updated": False,
                "reason": "version_mismatch",
            }
        payload = dict(updates)
        payload["version"] = expected_version + 1
        transaction.set(doc_ref, payload, merge=True)
        return {
            "document_id": document_id,
            "updated": True,
            "version": expected_version + 1,
        }

    transaction = client.transaction()
    return _txn(transaction)
