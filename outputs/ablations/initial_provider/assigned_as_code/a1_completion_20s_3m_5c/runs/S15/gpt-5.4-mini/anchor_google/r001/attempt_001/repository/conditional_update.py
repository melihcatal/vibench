from google.cloud import firestore
from database_client import get_firestore_client, load_config
from database_models import build_response


def conditional_update(payload, config=None):
    config = load_config(config)
    client = get_firestore_client(config)
    ref = client.collection(config["collection"]).document(payload["id"])
    updates = dict(payload["updates"])
    if "version" in payload:
        transaction = client.transaction()

        @firestore.transactional
        def update_in_transaction(transaction_obj):
            snapshot = ref.get(transaction=transaction_obj)
            current = snapshot.to_dict() if snapshot.exists else {}
            if current.get("version") != payload["version"]:
                return False
            transaction_obj.update(ref, updates)
            return True

        updated = update_in_transaction(transaction)
    else:
        ref.update(updates)
        updated = True
    return build_response(id=payload["id"], updated=updated)
