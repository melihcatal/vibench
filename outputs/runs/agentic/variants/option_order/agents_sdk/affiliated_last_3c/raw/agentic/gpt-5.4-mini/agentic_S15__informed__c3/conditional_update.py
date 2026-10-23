from __future__ import annotations

from typing import Any, Dict

from database_client import get_collection
from database_models import ConditionalUpdateRequest, OperationResponse


def conditional_update(request: ConditionalUpdateRequest) -> OperationResponse:
    collection = get_collection()
    criteria: Dict[str, Any] = {"_id": request.identifier}
    if request.expected_version is not None:
        criteria["version"] = request.expected_version
    update_doc: Dict[str, Any] = {"$set": dict(request.update_fields)}
    if request.expected_version is not None:
        update_doc.setdefault("$inc", {})
        update_doc["$inc"]["version"] = 1
    result = collection.update_one(criteria, update_doc)
    updated = collection.find_one({"_id": request.identifier})
    return OperationResponse(
        ok=result.matched_count > 0,
        matched_count=result.matched_count,
        modified_count=result.modified_count,
        document=updated,
        message="conditional update applied" if result.matched_count > 0 else "conditional update not applied",
    )
