from database_client import get_firestore_client
from database_models import Document


def query_documents(collection_name: str, field: str, value: any):
    """Queries documents by a field value in Google Firestore."""
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field, "==", value).stream()
    return [Document.from_dict(doc.id, doc.to_dict()) for doc in docs]
