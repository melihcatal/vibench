"""
upsert_document.py - Upserts a JSON document by its primary identifier
into MongoDB Atlas managed NoSQL document store.

Provider: MongoDB Atlas (pymongo driver for mongodb+srv:// clusters)
"""

from typing import Any, Dict

from database_client import AtlasClient
from database_models import (
    DocumentRecord,
    UpsertRequest,
    normalize_user_content,
    now_utc_iso,
)


def upsert_document(request: UpsertRequest) -> DocumentRecord:
    """
    Insert or update a document in MongoDB Atlas by its doc_id.
    Uses MongoDB Atlas upsert semantics (update_one with upsert=True).
    """
    now = now_utc_iso()
    cleaned_data = normalize_user_content(request.data)

    record = DocumentRecord(
        doc_id=request.doc_id,
        data=cleaned_data,
        partition_key=request.partition_key,
        version=1,
        created_at=now,
        updated_at=now,
        metadata=request.metadata or {},
    )

    with AtlasClient() as client:
        mongo_doc = record.to_mongo()
        client.insert_or_update(request.doc_id, mongo_doc)

    return record


def upsert_document_raw(
    doc_id: str,
    data: Dict[str, Any],
    partition_key: str = None,
    metadata: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Convenience wrapper accepting raw keyword arguments and returning
    a dict representation of the upserted document.
    """
    request = UpsertRequest(
        doc_id=doc_id,
        data=data,
        partition_key=partition_key,
        metadata=metadata,
    )
    result = upsert_document(request)
    return result.to_mongo()
