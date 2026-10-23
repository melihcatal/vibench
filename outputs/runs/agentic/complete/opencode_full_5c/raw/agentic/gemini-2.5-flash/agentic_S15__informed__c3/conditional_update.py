from database_client import get_firestore_client
from typing import Dict, Any


def conditional_update(
    document_id: str,
    collection_name: str,
    updates: Dict[str, Any],
    current_version: int,
) -> Dict[str, Any]:
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    # Use a transaction for a robust conditional update
    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, current_version):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist")

        doc_data = snapshot.to_dict()
        if doc_data.get("version") != current_version:
            raise ValueError("Document version mismatch. Update aborted.")

        new_version = current_version + 1
        updates["version"] = new_version
        transaction.update(doc_ref, updates)
        return {
            "status": "success",
            "document_id": document_id,
            "new_version": new_version,
        }

    transaction = db.transaction()
    try:
        return update_in_transaction(transaction, doc_ref, updates, current_version)
    except ValueError as e:
        return {"status": "failed", "message": str(e)}
