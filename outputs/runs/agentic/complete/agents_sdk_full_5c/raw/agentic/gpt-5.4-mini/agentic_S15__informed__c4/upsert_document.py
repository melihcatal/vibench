from typing import Any, Dict

from pymongo import ReturnDocument

from database_client import build_document_id, get_collection
from database_models import DocumentRequest, OperationResponse, normalize_document


def upsert_document(request: DocumentRequest) -> Dict[str, Any]:
    collection = get_collection(request.db_name, request.collection_name)
    document = normalize_document(request.document)
    document_id = build_document_id(document)
    document["_id"] = document_id
    result = collection.find_one_and_replace(
        {"_id": document_id},
        document,
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    response = OperationResponse(ok=True, provider="MongoDB Atlas", data={"document": result})
    return response.__dict__
