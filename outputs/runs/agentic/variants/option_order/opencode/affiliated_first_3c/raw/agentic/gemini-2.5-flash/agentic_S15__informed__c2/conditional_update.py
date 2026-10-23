from database_client import FirestoreClient
from database_models import DocumentConditionalUpdateRequest


def conditional_update(request: DocumentConditionalUpdateRequest):
    db = FirestoreClient.get_client()
    doc_ref = db.collection("documents").document(request.document_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, expected_version):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document not found")
        current_version = snapshot.get("version")

        if current_version != expected_version:
            raise ValueError("Version mismatch")

        new_version = current_version + 1
        updates["version"] = new_version
        transaction.update(doc_ref, updates)
        return new_version

    try:
        new_version = update_in_transaction(
            transaction, doc_ref, request.updates, request.expected_version
        )
        return {
            "status": "success",
            "document_id": request.document_id,
            "new_version": new_version,
        }
    except ValueError as e:
        return {"status": "failed", "message": str(e)}
