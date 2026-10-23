from typing import Any, Dict, Optional
import os
from google.cloud import firestore
from google.api_core.exceptions import NotFound


class FirestoreClient:
    def __init__(self) -> None:
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION", "documents")

    def conditional_update(
        self,
        document_id: str,
        condition_field: str,
        condition_value: Any,
        update_data: Dict[str, Any],
    ) -> bool:
        doc_ref = self.db.collection(self.collection_name).document(document_id)
        transaction = self.db.transaction()

        @firestore.transactional
        def update_in_transaction(transaction):
            snapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                return False
            if snapshot.get(condition_field) != condition_value:
                return False
            transaction.update(doc_ref, update_data)
            return True

        return update_in_transaction(transaction)
