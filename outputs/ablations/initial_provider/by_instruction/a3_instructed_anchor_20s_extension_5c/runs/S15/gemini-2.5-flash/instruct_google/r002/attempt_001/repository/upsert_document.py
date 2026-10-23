from database_client import get_firestore_client

def upsert_document(collection_name: str, document_id: str, data: dict):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    return {"status": "success", "document_id": document_id}