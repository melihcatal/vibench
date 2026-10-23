"""
Fetches a document by identifier from a MongoDB Atlas managed NoSQL document store.
Uses pymongo for MongoDB Atlas integration.
"""

from __future__ import annotations

from typing import Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from database_client import get_collection, create_mongo_client
from database_models import DocumentRecord, normalize_document_id


def fetch_document(
    doc_id: str,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
    include_metadata: bool = True,
) -> Optional[dict[str, Any]]:
    """
    Fetch a single document from MongoDB Atlas by its primary identifier.
    
    Args:
        doc_id: The unique primary identifier for the document.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
        include_metadata: Whether to include version, created_at, and updated_at fields.
    
    Returns:
        A dict containing the document content and optionally metadata, or None if not found.
    """
    if collection is None:
        collection = get_collection(client)

    normalized_id = normalize_document_id(doc_id)

    projection: dict[str, int] = {"_id": 1, "data": 1, "version": 1}
    if include_metadata:
        projection["created_at"] = 1
        projection["updated_at"] = 1
        projection["partition_key"] = 1

    raw_doc = collection.find_one({"_id": normalized_id}, projection)

    if raw_doc is None:
        return None

    record = DocumentRecord.from_mongo_document(raw_doc)
    result: dict[str, Any] = {
        "doc_id": record.doc_id,
        "content": record.content,
        "version": record.version,
    }
    if include_metadata:
        result["created_at"] = record.created_at
        result["updated_at"] = record.updated_at
        result["partition_key"] = record.partition_key

    return result


def fetch_documents_by_ids(
    doc_ids: list[str],
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
    include_metadata: bool = True,
) -> list[dict[str, Any]]:
    """
    Fetch multiple documents from MongoDB Atlas by their primary identifiers.
    
    Args:
        doc_ids: List of unique primary identifiers.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
        include_metadata: Whether to include metadata fields.
    
    Returns:
        List of dicts containing the fetched documents.
    """
    if collection is None:
        collection = get_collection(client)

    normalized_ids = [normalize_document_id(did) for did in doc_ids]

    projection: dict[str, int] = {"_id": 1, "data": 1, "version": 1}
    if include_metadata:
        projection["created_at"] = 1
        projection["updated_at"] = 1
        projection["partition_key"] = 1

    cursor = collection.find({"_id": {"$in": normalized_ids}}, projection)

    results = []
    for raw_doc in cursor:
        record = DocumentRecord.from_mongo_document(raw_doc)
        result: dict[str, Any] = {
            "doc_id": record.doc_id,
            "content": record.content,
            "version": record.version,
        }
        if include_metadata:
            result["created_at"] = record.created_at
            result["updated_at"] = record.updated_at
            result["partition_key"] = record.partition_key
        results.append(result)

    return results


def fetch_document_with_lock(
    doc_id: str,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> Optional[dict[str, Any]]:
    """
    Fetch a document from MongoDB Atlas with optimistic locking metadata.
    
    Returns the document along with its current version for subsequent conditional updates.
    
    Args:
        doc_id: The unique primary identifier for the document.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A dict with document content and version, or None if not found.
    """
    doc = fetch_document(doc_id, collection, client, include_metadata=True)
    if doc is None:
        return None

    return {
        "doc_id": doc["doc_id"],
        "content": doc["content"],
        "version": doc.get("version", 1),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


if __name__ == "__main__":
    client = create_mongo_client()
    try:
        doc = fetch_document("sample-001", client=client)
        print(doc)
    finally:
        client.close()
