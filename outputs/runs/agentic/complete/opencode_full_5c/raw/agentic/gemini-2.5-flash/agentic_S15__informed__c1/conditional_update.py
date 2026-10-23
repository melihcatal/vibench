from database_client import get_firestore_client
from google.cloud.firestore import Transaction, Client


def conditional_update(
    collection_name: str,
    document_id: str,
    new_data: dict,
    expected_field: str,
    expected_value: any,
):
    db: Client = get_firestore_client()
    document_ref = db.collection(collection_name).document(document_id)

    @firestore.transactional
    def update_in_transaction(
        transaction: Transaction,
        doc_ref,
        new_doc_data,
        expected_field_value,
        field_to_check,
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists and snapshot.get(field_to_check) == expected_field_value:
            transaction.update(doc_ref, new_doc_data)
            return {"status": "success", "document_id": document_id}
        else:
            return {"status": "condition_failed", "document_id": document_id}

    transaction = db.transaction()
    return update_in_transaction(
        transaction, document_ref, new_data, expected_value, expected_field
    )
