from google.cloud import firestore

from database_client import get_collection_ref
from database_models import normalize_document


def conditional_update(payload, config=None):
    config = config or {}
    payload = normalize_document(payload)
    ref = get_collection_ref(config).document(payload["id"])
    transaction = firestore.Client(project=config["project_id"]).transaction()

    @firestore.transactional
    def update_in_transaction(txn):
        snapshot = ref.get(transaction=txn)
        current = snapshot.to_dict() if snapshot.exists else None
        expected_version = payload.get("version")
        if expected_version is not None:
            if not current or current.get("version") != expected_version:
                return {"updated": False, "id": payload["id"]}
        txn.set(ref, payload["document"], merge=True)
        return {"updated": True, "id": payload["id"]}

    return update_in_transaction(transaction)
