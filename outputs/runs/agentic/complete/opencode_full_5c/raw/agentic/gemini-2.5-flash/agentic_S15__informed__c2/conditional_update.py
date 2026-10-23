from database_client import get_firestore_client, get_collection_name
from database_models import Document
from typing import Dict, Any, Optional


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    condition_field: str,
    condition_value: Any,
) -> Optional[Document]:
    """
    Applies a conditional update to one stored document in Google Firestore.
    The update only proceeds if `condition_field` in the document matches `condition_value`.
    """
    db = get_firestore_client()
    collection_name = get_collection_name()
    doc_ref = db.collection(collection_name).document(document_id)

    # Use a transaction for a robust conditional update
    @firestore.transactional
    def update_in_transaction(
        transaction, doc_ref, updates, condition_field, condition_value
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists and snapshot.get(condition_field) == condition_value:
            transaction.update(doc_ref, updates)
            updated_data = {**snapshot.to_dict(), **updates}
            return Document(id=document_id, data=updated_data)
        else:
            return None

    transaction = db.transaction()
    updated_document = update_in_transaction(
        transaction, doc_ref, updates, condition_field, condition_value
    )
    return updated_document
