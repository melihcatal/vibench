from google.cloud import firestore

def conditional_update(document_id, update_payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    doc_ref = client.collection(config["collection"]).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update(update_payload)
        return {"id": document_id}
    else:
        return None