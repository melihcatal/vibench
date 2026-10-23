"""
Local request, response, and normalization helpers for MongoDB Atlas document store.

Provider: MongoDB Atlas
SDK: pymongo
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def normalize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a document for insertion, stripping ObjectId serialization artifacts."""
    result = dict(doc)
    # Remove _id if it's a raw ObjectId string representation
    if "_id" in result and not isinstance(result["_id"], str):
        result["_id"] = str(result["_id"])
    # Ensure standard metadata fields
    result.setdefault("_created_at", datetime.utcnow().isoformat())
    result.setdefault("_updated_at", datetime.utcnow().isoformat())
    return result


def prepare_upsert_payload(
    document_id: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """Build the document payload for an upsert operation."""
    payload = normalize_document({"_id": document_id, **data})
    payload["_updated_at"] = datetime.utcnow().isoformat()
    return payload


def format_query_filter(
    partition_key: Optional[str] = None,
    field_name: Optional[str] = None,
    field_value: Optional[Any] = None,
    document_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a MongoDB filter dict from query parameters."""
    query_filter: Dict[str, Any] = {}
    if document_id is not None:
        query_filter["_id"] = document_id
    if partition_key is not None:
        query_filter["partition_key"] = partition_key
    if field_name is not None and field_value is not None:
        query_filter[field_name] = field_value
    return query_filter


def format_conditional_query(
    document_id: str,
    condition_field: str,
    condition_value: Any,
) -> Dict[str, Any]:
    """Build a MongoDB filter for a conditional/version-aware update."""
    return {"_id": document_id, condition_field: condition_value}


def build_update_payload(
    updates: Dict[str, Any],
    document_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the $set update payload with timestamp."""
    payload = dict(updates)
    payload["_updated_at"] = datetime.utcnow().isoformat()
    return {"$set": payload}


def normalize_query_results(
    raw_results: List[Dict[str, Any]],
    projection: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Normalize query results and optionally project specific fields."""
    results = []
    for doc in raw_results:
        record = normalize_document(doc)
        if projection:
            record = {k: record.get(k) for k in projection}
        results.append(record)
    return results


def build_response(
    success: bool,
    data: Optional[Any] = None,
    message: Optional[str] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a standardized response dictionary."""
    response = {"success": success, "timestamp": datetime.utcnow().isoformat()}
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    if error is not None:
        response["error"] = error
    return response
