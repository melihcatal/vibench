"""
Upserts a JSON document by its primary identifier into MongoDB Atlas.
Uses pymongo for MongoDB Atlas managed NoSQL document store integration.
"""

from __future__ import annotations

from typing import Any, Optional

from pymongo import MongoClient
from pymongo.results import UpdateResult
from pymongo.collection import Collection

from database_client import get_collection, create_mongo_client
from database_models import DocumentRecord, normalize_document_id, sanitize_for_mongo


def upsert_document(
    doc_id: str,
    content: dict[str, Any],
    partition_key: Optional[str] = None,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> dict[str, Any]:
    """
    Upsert a JSON document into a MongoDB Atlas collection by its primary identifier.
    
    Uses MongoDB Atlas replace_one with upsert=True to either insert a new document
    or replace an existing one identified by doc_id.
    
    Args:
        doc_id: The unique primary identifier for the document.
        content: The JSON document payload to store.
        partition_key: Optional partition key for sharded or partitioned collections.
        collection: Optional pre-configured pymongo Collection. If None, one is created.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A dict with the document id, upserted flag, and matched count.
    """
    if collection is None:
        collection = get_collection(client)

    normalized_id = normalize_document_id(doc_id)
    sanitized_content = sanitize_for_mongo(content)

    record = DocumentRecord(
        doc_id=normalized_id,
        content=sanitized_content,
        partition_key=partition_key,
    )

    update_payload = {
        "$set": {
            "data": sanitized_content,
            "updated_at": record.updated_at or record.created_at,
            "version": record.version,
        },
        "$setOnInsert": {
            "_id": normalized_id,
            "created_at": record.created_at,
        },
    }

    if partition_key:
        update_payload["$set"]["partition_key"] = partition_key

    result: UpdateResult = collection.update_one(
        {"_id": normalized_id},
        update_payload,
        upsert=True,
    )

    return {
        "doc_id": normalized_id,
        "upserted": result.upserted_id is not None,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }


def upsert_documents_batch(
    documents: list[dict[str, Any]],
    id_field: str = "doc_id",
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> list[dict[str, Any]]:
    """
    Batch upsert multiple documents into MongoDB Atlas.
    
    Args:
        documents: List of dicts, each containing an id_field and a 'content' key.
        id_field: The key in each dict that serves as the primary identifier.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        List of result dicts for each upserted document.
    """
    results = []
    if collection is None:
        collection = get_collection(client)

    for doc in documents:
        doc_id = normalize_document_id(doc.get(id_field))
        content = doc.get("content", {})
        partition_key = doc.get("partition_key")
        result = upsert_document(
            doc_id=doc_id,
            content=content,
            partition_key=partition_key,
            collection=collection,
        )
        results.append(result)

    return results


if __name__ == "__main__":
    client = create_mongo_client()
    try:
        result = upsert_document(
            doc_id="sample-001",
            content={"title": "Sample Document", "status": "active", "tags": ["demo"]},
            client=client,
        )
        print(result)
    finally:
        client.close()
