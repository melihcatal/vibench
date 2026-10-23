from database_client import get_firestore_client
from google.cloud.firestore import Transaction


def conditional_update(
    collection_name: str,
    document_id: str,
    field_to_check: str,
    expected_value: any,
    new_data: dict,
):
    db = get_firestore_client()
    transaction = db.transaction()
    doc_ref = db.collection(collection_name).document(document_id)

    @Transaction.run_in_transaction(transaction)
    def update_in_transaction(
        transaction, doc_ref, field_to_check, expected_value, new_data
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist!")

        if snapshot.get(field_to_check) == expected_value:
            transaction.update(doc_ref, new_data)
            return {"message": f"Document {document_id} updated successfully."}
        else:
            raise ValueError("Conditional update failed: field value mismatch.")

    try:
        return update_in_transaction(
            transaction, doc_ref, field_to_check, expected_value, new_data
        )
    except ValueError as e:
        return {"error": str(e)}
