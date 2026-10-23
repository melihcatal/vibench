from database_client import get_collection
from database_models import (
    DocumentRequest,
    DocumentResponse,
    normalize_document,
    to_document_response,
)


def upsert_document(request: DocumentRequest) -> DocumentResponse:
    collection = get_collection()
    doc_data = normalize_document(request.data, request.document_id)
    doc_data["partition_key"] = request.partition_key
    doc_data["version"] = doc_data.get("version", 0) + 1

    result = collection.update_one(
        {"_id": request.document_id},
        {"$set": doc_data},
        upsert=True,
    )

    if result.upserted_id is not None:
        doc_data["_id"] = result.upserted_id

    return to_document_response(doc_data)
