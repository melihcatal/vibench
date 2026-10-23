from database_client import get_firestore_client

def fetch_document(payload, config=None):
    config = config or {}
    client = get_firestore_client(project_id=config["project_id"])
    doc_ref = client.collection(config["collection"]).document(payload["id"])
    document = doc_ref.get()
    if document.exists:
        return {"id": document.id, "document": document.to_dict()}
    else:
        return {"id": payload["id"], "document": None}
