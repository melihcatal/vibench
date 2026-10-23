from google.cloud import firestore

def fetch_document(document_id, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    document_ref = client.collection(config["collection"]).document(document_id)
    document = document_ref.get()
    if document.exists:
        return document.to_dict()
    else:
        return None