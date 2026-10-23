from google.cloud import firestore

def conditional_update(document_id, update_payload, condition_payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    document_ref = client.collection(config["collection"]).document(document_id)
    document = document_ref.get()
    if document.exists and document.to_dict() == condition_payload:
        document_ref.update(update_payload)
        return {"id": document_id}
    else:
        return None