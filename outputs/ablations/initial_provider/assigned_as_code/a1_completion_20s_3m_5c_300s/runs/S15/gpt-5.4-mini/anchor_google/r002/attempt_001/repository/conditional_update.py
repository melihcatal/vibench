from google.cloud import firestore

from database_client import load_config


def conditional_update(payload, config=None):
    config = load_config(config)
    client = firestore.Client(project=config["project_id"])
    doc_ref = client.collection(config["collection"]).document(payload["id"])
    version = payload.get("version")
    updates = dict(payload["updates"])

    @firestore.transactional
    def update_in_transaction(transaction):
        snapshot = doc_ref.get(transaction=transaction)
        current = snapshot.to_dict() or {}
        if version is not None and current.get("version") != version:
            raise ValueError("version_mismatch")
        next_version = (current.get("version") or 0) + 1
        updates_with_version = dict(updates)
        updates_with_version["version"] = next_version
        transaction.update(doc_ref, updates_with_version)
        return {"id": payload["id"], "version": next_version}

    transaction = client.transaction()
    return update_in_transaction(transaction)
