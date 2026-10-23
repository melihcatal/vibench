from database_client import get_firestore_client
from database_models import Document


def query_documents(collection_name: str, field_name: str, field_value: str):
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    results = []
    for doc in docs:
        results.append(Document.from_dict(doc).to_dict())
    return {"status": "success", "documents": results}
