import os

from google.cloud import firestore

from database_client import get_firestore_client
from database_models import ConditionalUpdateRequest


def conditional_update(request: ConditionalUpdateRequest):
    client = get_firestore_client()
    ref = client.collection(request.collection).document(request.document_id)
    transaction = client.transaction()

    @firestore.transactional
    def apply(transaction_obj):
        snapshot = ref.get(transaction=transaction_obj)
        if not snapshot.exists:
            raise ValueError("not found")
        data = snapshot.to_dict() or {}
        if request.expected_version is not None and data.get(request.version_field) != request.expected_version:
            raise ValueError("version mismatch")
        new_data = dict(data)
        new_data.update(request.updates)
        if request.expected_version is not None:
            new_data[request.version_field] = request.expected_version + 1
        transaction_obj.set(ref, new_data, merge=False)
        return new_data

    updated = apply(transaction)
    return {"ok": True, "document": updated}


def main():
    request = ConditionalUpdateRequest(collection=os.getenv("FIRESTORE_COLLECTION", "documents"), document_id="sample", updates={"status": "updated"}, expected_version=1)
    return conditional_update(request)


if __name__ == "__main__":
    main()
