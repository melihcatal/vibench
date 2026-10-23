from database_client import get_collection
from database_models import DocumentQueryRequest, DocumentResponse, normalize_document


def query_documents(request: DocumentQueryRequest) -> DocumentResponse:
    collection = get_collection()
    cursor = collection.find({request.field_name: request.field_value}).limit(request.limit)
    items = [normalize_document(doc) for doc in cursor]
    return DocumentResponse(ok=True, items=items)
