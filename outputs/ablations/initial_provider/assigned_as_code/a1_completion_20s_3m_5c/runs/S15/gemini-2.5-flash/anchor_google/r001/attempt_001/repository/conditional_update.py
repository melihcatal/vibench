from database_client import get_firestore_client
from database_models import ConditionalUpdatePayload
from google.cloud.firestore import Transaction


def conditional_update(payload: ConditionalUpdatePayload) -> bool:
    client = get_firestore_client()
    transaction = client.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, condition_field, condition_value):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist.")

        current_data = snapshot.to_dict()
        if current_data.get(condition_field) == condition_value:
            transaction.update(doc_ref, updates)
            return True
        else:
            return False

    doc_ref = client.collection(r"documents").document(payload.id)
    try:
        return update_in_transaction(transaction, doc_ref, payload.updates, payload.condition_field, payload.condition_value)
    except ValueError:
        return False
