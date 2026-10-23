from google.cloud import firestore


def conditional_update(document_id, update_data, condition, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    document_ref = client.collection(config["collection"]).document(document_id)
    document = document_ref.get()
    if document.exists and eval(condition):
        document_ref.update(update_data)
        return {"id": document_id}
    else:
        return None