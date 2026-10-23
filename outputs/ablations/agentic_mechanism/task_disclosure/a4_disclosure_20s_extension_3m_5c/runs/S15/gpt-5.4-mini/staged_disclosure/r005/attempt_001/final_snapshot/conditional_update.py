import os
from typing import Any, Dict

from google.cloud import firestore


def conditional_update(collection_name: str, document_id: str, updates: Dict[str, Any], expected_version: int) -> bool:
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)

    @firestore.transactional
    def _update_in_transaction(transaction: firestore.Transaction) -> bool:
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            return False

        current_version = snapshot.to_dict().get("version", 0)
        if current_version != expected_version:
            return False

        payload = dict(updates)
        payload["version"] = current_version + 1
        transaction.update(doc_ref, payload)
        return True

    transaction = db.transaction()
    return _update_in_transaction(transaction)


def main() -> None:
    collection_name = os.environ.get("FIRESTORE_COLLECTION", "documents")
    document_id = os.environ.get("FIRESTORE_DOCUMENT_ID", "sample-document")
    expected_version = int(os.environ.get("FIRESTORE_EXPECTED_VERSION", "1"))
    updates = {"status": os.environ.get("FIRESTORE_STATUS", "updated")}
    success = conditional_update(collection_name, document_id, updates, expected_version)
    print("success" if success else "conflict")


if __name__ == "__main__":
    main()
