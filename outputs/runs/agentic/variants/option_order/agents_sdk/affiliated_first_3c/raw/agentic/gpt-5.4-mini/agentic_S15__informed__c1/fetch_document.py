from database_client import get_collection
from database_models import DocumentFetchRequest, DocumentResponse, normalize_document


def fetch_document(request: DocumentFetchRequest) -> DocumentResponse:
    collection = get_collection()
    document = collection.find_one({request.primary_key: request.identifier})
    if not document:
        return DocumentResponse(ok=False, error="Document not found")
    return DocumentResponse(ok=True, data=normalize_document(document))
