from typing import Any, Dict, List, Optional

from database_client import get_collection
from database_models import DocumentRequest, DocumentResponse, normalize_mongo_id


def fetch_document(
    document_id: str,
    partition_key: Optional[str] = None,
    fields: Optional[List[str]] = None,
    collection_name: Optional[str] = None,
    database_name: Optional[str] = None,
) -> DocumentResponse:
    request = DocumentRequest(
        document_id=document_id,
        partition_key=partition_key,
        fields=fields,
    )

    collection = get_collection(collection_name, database_name)
    filter_query = request.to_mongo_filter()

    projection = None
    if fields:
        projection = {f: 1 for f in fields}
        projection["_id"] = 1

    try:
        doc = collection.find_one(filter_query, projection)

        if doc is None:
            return DocumentResponse(
                success=False,
                error=f"Document with id '{document_id}' not found",
            )

        normalized = normalize_mongo_id(doc)

        return DocumentResponse(
            success=True,
            document=normalized,
        )
    except Exception as exc:
        return DocumentResponse(
            success=False,
            error=f"Fetch error: {exc}",
        )
