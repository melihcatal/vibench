from typing import Any, Dict

from pymongo import UpdateOne

from database_client import get_collection, normalize_document
from database_models import DocumentRequest, DocumentResponse


def upsert_document(document_id: str, payload: Dict[str, Any]) -> DocumentResponse:
    collection = get_collection()
    request = DocumentRequest(document_id=document_id, payload=payload)
    record = dict(request.payload)
    record["document_id"] = request.document_id
    result = collection.replace_one({"document_id": request.document_id}, record, upsert=True)
    stored = collection.find_one({"document_id": request.document_id})
    return DocumentResponse(
        found=stored is not None,
        document=normalize_document(stored),
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        version=stored.get("version") if stored else None,
    )
