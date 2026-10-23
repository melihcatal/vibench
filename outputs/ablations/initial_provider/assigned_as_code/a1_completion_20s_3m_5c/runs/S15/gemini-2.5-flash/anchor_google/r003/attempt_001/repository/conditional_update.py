from database_client import get_firestore_client
from google.cloud.firestore import Transaction

def conditional_update(payload, config=None):
    config = config or {}
    client = get_firestore_client(project_id=config["project_id"])
    doc_ref = client.collection(config["collection"]).document(payload["id"])

    transaction = client.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, payload):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist")
        
        current_data = snapshot.to_dict()
        if current_data.get(payload["condition_field"]) == payload["condition_value"]:
            new_data = current_data
            new_data[payload["field"]] = payload["value"]
            transaction.set(doc_ref, new_data)
            return {"id": payload["id"], "status": "updated"}
        else:
            return {"id": payload["id"], "status": "condition_mismatch"}

    try:
        return update_in_transaction(transaction, doc_ref, payload)
    except ValueError as e:
        return {"id": payload["id"], "status": "error", "message": str(e)}
