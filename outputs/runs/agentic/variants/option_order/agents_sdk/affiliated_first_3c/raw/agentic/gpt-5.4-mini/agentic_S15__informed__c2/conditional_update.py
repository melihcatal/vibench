from typing import Any, Dict

from database_client import get_collection, normalize_document
from database_models import ConditionalUpdateRequest, DocumentResponse


def conditional_update(document_id: str, expected_version: int, updates: Dict[str, Any]) -> DocumentResponse:
    collection = get_collection()
    request = ConditionalUpdateRequest(document_id=document_id, expected_version=expected_version, updates=updates)
    update_fields = dict(request.updates)
    update_fields["version"] = request.expected_version + 1
    result = collection.update_one(
        {"document_id": request.document_id, "version": request.expected_version},
        {"$set": update_fields},
    )
    stored = collection.find_one({"document_id": request.document_id})
    return DocumentResponse(
        found=stored is not None,
        document=normalize_document(stored),
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        version=stored.get("version") if stored else None,
    )
