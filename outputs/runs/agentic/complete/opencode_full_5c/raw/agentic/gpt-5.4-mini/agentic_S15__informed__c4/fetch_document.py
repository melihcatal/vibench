from database_client import get_collection
from database_models import DocumentFetchRequest, DocumentResponse, normalize_identifier


def fetch_document(request: DocumentFetchRequest) -> DocumentResponse:
    collection = get_collection()
    document_id = normalize_identifier(request.document_id)
    query = {"id": document_id}
    if request.partition_key is not None:
        query["partition_key"] = request.partition_key
    document = collection.find_one(query, {"_id": 0})
    return DocumentResponse(
        ok=document is not None,
        document=document,
        error=None if document else "not found",
    )
