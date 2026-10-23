"""
Applies a conditional or version-aware update to one stored document in MongoDB Atlas.
Uses pymongo for MongoDB Atlas managed NoSQL document store integration.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import UpdateResult

from database_client import get_collection, create_mongo_client
from database_models import ConditionalUpdateSpec, DocumentRecord, sanitize_for_mongo


class ConditionalUpdateError(Exception):
    """Raised when a conditional update fails due to version mismatch or missing field."""
    pass


def conditional_update_document(
    doc_id: str,
    updates: dict[str, Any],
    expected_version: Optional[int] = None,
    required_field: Optional[str] = None,
    required_field_value: Optional[Any] = None,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> dict[str, Any]:
    """
    Apply a conditional, version-aware update to a document in MongoDB Atlas.
    
    The update will only succeed if:
    - The document exists and matches the expected version (optimistic concurrency).
    - A required field exists or matches an expected value.
    
    Args:
        doc_id: The primary identifier of the document to update.
        updates: A dict of field-value pairs to update within the document's data.
        expected_version: The expected current version number for optimistic concurrency.
        required_field: A field path within 'data' that must exist.
        required_field_value: An expected value for the required field.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A dict with the update result details.
    
    Raises:
        ConditionalUpdateError: If the update conditions are not met.
    """
    if collection is None:
        collection = get_collection(client)

    spec = ConditionalUpdateSpec(
        doc_id=doc_id,
        updates=sanitize_for_mongo(updates),
        expected_version=expected_version,
        required_field=required_field,
        required_field_value=required_field_value,
    )

    update_filter = spec.to_mongo_update_filter()
    update_payload = spec.to_mongo_update_payload()

    result: UpdateResult = collection.update_one(update_filter, update_payload)

    if result.matched_count == 0:
        error_parts = [f"Document '{doc_id}' not found or conditions not met."]
        if expected_version is not None:
            error_parts.append(f"Expected version {expected_version} may not match current version.")
        if required_field is not None:
            error_parts.append(f"Required field '{required_field}' check failed.")
        raise ConditionalUpdateError(" ".join(error_parts))

    new_version = expected_version + 1 if expected_version is not None else 2

    return {
        "doc_id": doc_id,
        "matched": True,
        "modified": result.modified_count > 0,
        "new_version": new_version,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def conditional_update_fields(
    doc_id: str,
    field_updates: dict[str, Any],
    expected_version: Optional[int] = None,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> dict[str, Any]:
    """
    Update specific fields within a document's data in MongoDB Atlas conditionally.
    
    This merges the provided field updates into the existing document data rather than
    replacing the entire data payload.
    
    Args:
        doc_id: The primary identifier of the document.
        field_updates: A dict of dot-notation or top-level field updates for the 'data' subdocument.
        expected_version: The expected current version for optimistic concurrency.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A dict with the update result details.
    """
    if collection is None:
        collection = get_collection(client)

    mongo_filter: dict[str, Any] = {"_id": doc_id}
    if expected_version is not None:
        mongo_filter["version"] = expected_version

    set_clause: dict[str, Any] = {}
    for field_path, value in field_updates.items():
        set_clause[f"data.{field_path}"] = sanitize_for_mongo(value)

    set_clause["updated_at"] = datetime.now(timezone.utc).isoformat()
    new_version = expected_version + 1 if expected_version is not None else 2
    set_clause["version"] = new_version

    result: UpdateResult = collection.update_one(
        mongo_filter,
        {"$set": set_clause},
    )

    if result.matched_count == 0:
        raise ConditionalUpdateError(
            f"Document '{doc_id}' not found or version {expected_version} mismatch."
        )

    return {
        "doc_id": doc_id,
        "matched": True,
        "modified": result.modified_count > 0,
        "new_version": new_version,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def delete_document_conditionally(
    doc_id: str,
    expected_version: Optional[int] = None,
    collection: Optional[Collection] = None,
    client: Optional[MongoClient] = None,
) -> dict[str, Any]:
    """
    Conditionally delete a document from MongoDB Atlas if version matches.
    
    Args:
        doc_id: The primary identifier of the document to delete.
        expected_version: The expected current version for optimistic concurrency.
        collection: Optional pre-configured pymongo Collection.
        client: Optional pre-configured pymongo MongoClient.
    
    Returns:
        A dict with the delete result details.
    
    Raises:
        ConditionalUpdateError: If the delete conditions are not met.
    """
    if collection is None:
        collection = get_collection(client)

    mongo_filter: dict[str, Any] = {"_id": doc_id}
    if expected_version is not None:
        mongo_filter["version"] = expected_version

    result = collection.delete_one(mongo_filter)

    if result.deleted_count == 0:
        raise ConditionalUpdateError(
            f"Document '{doc_id}' not found or version {expected_version} mismatch."
        )

    return {
        "doc_id": doc_id,
        "deleted": True,
        "version_at_deletion": expected_version,
        "deleted_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    client = create_mongo_client()
    try:
        result = conditional_update_document(
            doc_id="sample-001",
            updates={"status": "inactive"},
            expected_version=1,
            client=client,
        )
        print(result)
    except ConditionalUpdateError as e:
        print(f"Update failed: {e}")
    finally:
        client.close()
