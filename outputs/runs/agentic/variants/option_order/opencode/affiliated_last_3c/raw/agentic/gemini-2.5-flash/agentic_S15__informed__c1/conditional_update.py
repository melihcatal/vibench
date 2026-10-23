from database_client import get_firestore_client
from database_models import DocumentUpdate
from google.cloud.firestore import Transaction
from typing import Dict, Any, Optional


def conditional_update(
    collection_name: str, document_update: DocumentUpdate
) -> Dict[str, Any]:
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_update.id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, if_match: Optional[str]):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError(f"Document {document_update.id} does not exist.")

        current_data = snapshot.to_dict()

        if if_match:
            # Simulate version-aware update: check against a 'version' field
            # In a real scenario, 'if_match' might be an ETag or a specific version number.
            if current_data.get("version") != if_match:
                raise ValueError(
                    f"Document version mismatch. Expected {if_match}, got {current_data.get('version')}"
                )

            # If a version field is used, increment it for the next update
            updates["version"] = current_data.get("version", 0) + 1

        transaction.update(doc_ref, updates)
        return {"status": "success", "document_id": document_update.id}

    try:
        return update_in_transaction(
            transaction, doc_ref, document_update.updates, document_update.if_match
        )
    except ValueError as e:
        return {"status": "failed", "document_id": document_update.id, "error": str(e)}
