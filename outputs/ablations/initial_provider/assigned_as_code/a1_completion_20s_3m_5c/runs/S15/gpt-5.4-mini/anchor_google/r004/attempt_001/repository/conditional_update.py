from google.cloud import firestore

from database_client import load_config
from database_models import build_document_response


def conditional_update(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    ref = client.collection(config["collection"]).document(payload["id"])
    transaction = client.transaction()

    @firestore.transactional
    def apply_update(txn):
        snapshot = ref.get(transaction=txn)
        current = snapshot.to_dict() or {}
        expected_version = payload.get("expected_version")
        if expected_version is not None and current.get("version") != expected_version:
            return None
        updated = dict(current)
        updated.update(payload["updates"])
        if "version" in current:
            updated["version"] = current.get("version", 0) + 1
        txn.set(ref, updated)
        return updated

    result = apply_update(transaction)
    if result is None:
        return {"id": payload["id"], "updated": False}
    return build_document_response(payload["id"], result)
