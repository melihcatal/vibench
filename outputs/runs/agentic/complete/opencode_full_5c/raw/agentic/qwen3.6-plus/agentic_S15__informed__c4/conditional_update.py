from typing import Any, Dict, Optional

from pymongo.errors import WriteError

from database_client import get_collection
from database_models import (
    ConditionalUpdateRequest,
    DocumentResponse,
    normalize_mongo_id,
)


def conditional_update(
    document_id: str,
    update_fields: Dict[str, Any],
    condition: Optional[Dict[str, Any]] = None,
    version: Optional[int] = None,
    partition_key: Optional[str] = None,
    collection_name: Optional[str] = None,
    database_name: Optional[str] = None,
) -> DocumentResponse:
    request = ConditionalUpdateRequest(
        document_id=document_id,
        update_fields=update_fields,
        condition=condition,
        version=version,
        partition_key=partition_key,
    )

    collection = get_collection(collection_name, database_name)
    filter_query = request.to_mongo_filter()
    update_doc = request.to_mongo_update()

    try:
        result = collection.update_one(filter_query, update_doc)

        if result.matched_count == 0:
            return DocumentResponse(
                success=False,
                matched_count=0,
                modified_count=0,
                error="No document matched the filter and condition criteria",
            )

        updated_doc = collection.find_one({"_id": document_id})
        normalized = normalize_mongo_id(updated_doc) if updated_doc else None

        return DocumentResponse(
            success=True,
            document=normalized,
            matched_count=result.matched_count,
            modified_count=result.modified_count,
        )
    except WriteError as exc:
        return DocumentResponse(
            success=False,
            error=f"Conditional update write error: {exc}",
        )
    except Exception as exc:
        return DocumentResponse(
            success=False,
            error=f"Conditional update error: {exc}",
        )
