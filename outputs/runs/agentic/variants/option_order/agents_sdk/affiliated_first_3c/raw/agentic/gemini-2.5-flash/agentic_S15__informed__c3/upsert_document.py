from database_client import get_firestore_client
from database_models import Document

def upsert_document(collection_name: str, doc: Document):
    """
    Upserts (inserts or updates) a JSON document in Google Firestore.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(doc.id)
    doc_ref.set(doc.data)
    return {"status": "success", "document_id": doc.id}

if __name__ == "__main__":
    # Example usage
    sample_doc = Document("doc123", {"name": "Test Document", "value": 100})
    response = upsert_document("my_collection", sample_doc)
    print(f"Upserted document: {response}")
