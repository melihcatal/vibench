from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from database_client import get_collection
from database_models import UpdateResult, build_conditional_filter
from pymongo.collection import Collection


def conditional_update(
    document_id: str,
    updates: dict[str, Any],
    condition_field: str = "version",
    condition_operator: str = "eq",
    condition_value: Any = None,
    collection: Collection | None = None,
) -> UpdateResult:
    if collection is None:
        collection = get_collection()

    query_filter: dict[str, Any] = {"_id": document_id}

    if condition_value is not None:
        cond = build_conditional_filter(
            condition_field, condition_operator, condition_value
        )
        query_filter.update(cond)

    update_payload = {"$set": updates}
    update_payload["$set"]["updated_at"] = datetime.now(timezone.utc)

    if condition_field == "version" and condition_value is not None:
        new_version = condition_value + 1
        update_payload["$set"]["version"] = new_version
    else:
        new_version = None

    result = collection.update_one(query_filter, update_payload)

    return UpdateResult(
        document_id=document_id,
        matched=result.matched_count > 0,
        modified=result.modified_count > 0,
        new_version=new_version,
    )
