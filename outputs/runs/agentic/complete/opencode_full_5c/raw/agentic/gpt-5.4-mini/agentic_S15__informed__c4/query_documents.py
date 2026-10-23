from database_client import get_collection
from database_models import DocumentQueryRequest, DocumentResponse


def query_documents(request: DocumentQueryRequest) -> DocumentResponse:
    collection = get_collection()
    cursor = collection.find(
        {request.field_name: request.field_value}, {"_id": 0}
    ).limit(max(1, request.limit))
    documents = list(cursor)
    return DocumentResponse(ok=True, documents=documents)
