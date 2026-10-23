from database_client import get_collection, normalize_document
from database_models import DocumentResponse


def fetch_document(document_id: str) -> DocumentResponse:
    collection = get_collection()
    stored = collection.find_one({"document_id": document_id})
    return DocumentResponse(found=stored is not None, document=normalize_document(stored), version=stored.get("version") if stored else None)
