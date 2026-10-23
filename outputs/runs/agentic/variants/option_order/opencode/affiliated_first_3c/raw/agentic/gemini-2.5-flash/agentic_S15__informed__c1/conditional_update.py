from database_client import get_firestore_client, get_collection_name
from database_models import Document
from google.cloud.firestore import Transaction
from typing import Any, Dict, Optional


def conditional_update(
    document_id: str, updates: Dict[str, Any], expected_version: int
) -> Optional[Document]:
    db = get_firestore_client()
    collection_ref = db.collection(get_collection_name())
    doc_ref = collection_ref.document(document_id)

    @firestore.transactional
    def update_in_transaction(
        transaction: Transaction, doc_ref, updates, expected_version
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            return None  # Document does not exist

        current_data = snapshot.to_dict()
        current_version = current_data.get("version")

        if current_version != expected_version:
            raise ValueError(
                "Version mismatch: document has been modified by another process."
            )

        new_version = expected_version + 1
        updates["version"] = new_version
        transaction.update(doc_ref, updates)

        updated_data = {**current_data, **updates}
        return Document(id=document_id, data=updated_data, version=new_version)

    try:
        return update_in_transaction(
            db.transaction(), doc_ref, updates, expected_version
        )
    except ValueError as e:
        print(f"Conditional update failed: {e}")
        return None
