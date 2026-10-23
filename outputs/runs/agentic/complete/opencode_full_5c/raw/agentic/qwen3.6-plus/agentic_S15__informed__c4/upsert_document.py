from typing import Any, Dict, Optional
from pymongo.errors import DuplicateKeyError, WriteError

from database_client import get_collection
from database_models import DocumentRequest, DocumentResponse


def upsert_document(
    document_id: str,
    data: Dict[str, Any],
    partition_key: Optional[str] = None,
    collection_name: Optional[str] = None,
    database_name: Optional[str] = None,
) -> DocumentResponse:
    request = DocumentRequest(
        document_id=document_id,
        data=data,
        partition_key=partition_key,
    )

    collection = get_collection(collection_name, database_name)
    filter_query = request.to_mongo_filter()
    payload = request.to_upsert_payload()

    try:
        result = collection.replace_one(
            filter_query,
            payload,
            upsert=True,
        )

        upserted_id = str(result.upserted_id) if result.upserted_id else None

        return DocumentResponse(
            success=True,
            document=payload,
            matched_count=result.matched_count,
            modified_count=result.modified_count,
            upserted_id=upserted_id,
        )
    except DuplicateKeyError as exc:
        return DocumentResponse(
            success=False,
            error=f"Duplicate key error: {exc}",
        )
    except WriteError as exc:
        return DocumentResponse(
            success=False,
            error=f"Write error: {exc}",
        )
