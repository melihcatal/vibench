from google.cloud import firestore


def conditional_update(document_id, update_payload, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    document_ref = client.collection(config["collection"]).document(document_id)
    document = document_ref.get()
    if document.exists:
        document_ref.update(update_payload)
        return document_ref.get().to_dict()
    else:
        return None