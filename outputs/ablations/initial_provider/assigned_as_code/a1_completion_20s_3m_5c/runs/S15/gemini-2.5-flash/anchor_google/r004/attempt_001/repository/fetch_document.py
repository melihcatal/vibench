from database_client import get_firestore_client

def fetch_document(document_id, collection_name, project_id):
    client = get_firestore_client(project_id)
    doc_ref = client.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"id": doc.id, "document": doc.to_dict()}
    else:
        return None
