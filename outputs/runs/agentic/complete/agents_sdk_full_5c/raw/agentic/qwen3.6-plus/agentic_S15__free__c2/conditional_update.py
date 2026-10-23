"""
Apply a conditional or version-aware update to a stored document in a MongoDB Atlas managed NoSQL document store.
Uses the official PyMongo SDK (pymongo) for MongoDB Atlas integration.
"""

from typing import Dict, Any, Optional

from pymongo.collection import Collection

from database_client import get_collection
from database_models import (
    ConditionalUpdateRequest,
    build_conditional_update_result,
    normalize_document_result,
    DocumentResponse,
)


def conditional_update(
    collection_name: str,
    document_id: str,
    update_fields: Dict[str, Any],
    required_version: Optional[int] = None,
    client=None,
) -> Dict[str, Any]:
    """
    Apply a conditional update to a document in MongoDB Atlas,
    optionally gated on the current document version (optimistic concurrency).

    Args:
        collection_name: Name of the MongoDB collection.
        document_id: The document's primary identifier.
        update_fields: Fields to update (merged into the document).
        required_version: If set, the update only proceeds when the document's
                          current _metadata.version matches this value.
        client: Optional pre-configured MongoClient instance.

    Returns:
        A dict with keys: success (bool), updated_version (int|None), error (str|None).
    """
    request = ConditionalUpdateRequest(
        collection_name=collection_name,
        document_id=document_id,
        update_fields=update_fields,
        required_version=required_version,
    )

    collection = get_collection(collection_name, client=client)

    try:
        filter_query: Dict[str, Any] = {"_id": document_id}

        if request.required_version is not None:
            filter_query["_metadata.version"] = request.required_version

        new_version = (request.required_version or 0) + 1

        update_doc = {
            "$set": {
                **update_fields,
                "_metadata.updated_at": __import__("datetime").datetime.utcnow().isoformat(),
                "_metadata.version": new_version,
            }
        }

        result = collection.update_one(filter_query, update_doc)

        if result.matched_count == 0:
            if request.required_version is not None:
                return build_conditional_update_result(
                    success=False,
                    error="Version conflict: document not at the expected version",
                )
            return build_conditional_update_result(
                success=False,
                error="Document not found",
            )

        return build_conditional_update_result(
            success=True,
            updated_version=new_version,
        )

    except Exception as exc:
        return build_conditional_update_result(
            success=False,
            error=str(exc),
        )


def conditional_set_field(
    collection_name: str,
    document_id: str,
    field_path: str,
    new_value: Any,
    required_version: Optional[int] = None,
    client=None,
) -> Dict[str, Any]:
    """
    Convenience helper to set a single field (possibly nested) conditionally
    on a document in MongoDB Atlas.

    Args:
        collection_name: Name of the MongoDB collection.
        document_id: The document's primary identifier.
        field_path: Dot-notation field path (e.g., "content.title").
        new_value: The new value for the field.
        required_version: Optional version gate.
        client: Optional pre-configured MongoClient instance.

    Returns:
        Result dict from conditional_update.
    """
    return conditional_update(
        collection_name=collection_name,
        document_id=document_id,
        update_fields={field_path: new_value},
        required_version=required_version,
        client=client,
    )


if __name__ == "__main__":
    result = conditional_update(
        collection_name="documents",
        document_id="doc-001",
        update_fields={"status": "archived"},
        required_version=1,
    )
    print(result)
