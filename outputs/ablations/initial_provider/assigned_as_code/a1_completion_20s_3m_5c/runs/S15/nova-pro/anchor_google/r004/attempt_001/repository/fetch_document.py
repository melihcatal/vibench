from google.cloud import firestore

def fetch_document(document_id, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    doc_ref = client.collection(config["collection"]).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None