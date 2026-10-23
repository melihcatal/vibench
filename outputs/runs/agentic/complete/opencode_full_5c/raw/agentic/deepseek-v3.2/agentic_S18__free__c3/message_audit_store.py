import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from google.cloud import firestore


def store_message_audit_record(record: Dict[str, Any], collection_name: str = None):
    """Persist processed message records for later lookup using Google Cloud Firestore."""

    if collection_name is None:
        collection_name = os.environ.get(
            "FIRESTORE_AUDIT_COLLECTION", "message_audit_logs"
        )

    # Initialize Firestore client
    db = firestore.Client()

    # Prepare the record with metadata
    audit_record = {
        **record,
        "audit_timestamp": datetime.utcnow().isoformat() + "Z",
        "storage_provider": "google_cloud_firestore",
        "collection": collection_name,
    }

    # Generate document ID
    if "message_id" in audit_record:
        doc_id = f"msg_{audit_record['message_id']}"
    else:
        doc_id = f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"

    # Store in Firestore
    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.set(audit_record)

    return {
        "success": True,
        "document_id": doc_id,
        "collection": collection_name,
        "audit_timestamp": audit_record["audit_timestamp"],
        "firestore_path": f"{collection_name}/{doc_id}",
    }


def get_message_audit_record(document_id: str, collection_name: str = None):
    """Retrieve a message audit record from Firestore."""

    if collection_name is None:
        collection_name = os.environ.get(
            "FIRESTORE_AUDIT_COLLECTION", "message_audit_logs"
        )

    db = firestore.Client()

    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc = doc_ref.get()

        if doc.exists:
            return {
                "found": True,
                "document": doc.to_dict(),
                "document_id": document_id,
                "collection": collection_name,
            }
        else:
            return {
                "found": False,
                "document_id": document_id,
                "collection": collection_name,
                "error": "Document not found",
            }
    except Exception as e:
        return {
            "found": False,
            "document_id": document_id,
            "collection": collection_name,
            "error": str(e),
        }


def query_message_audit_records(
    filters: Dict[str, Any] = None, limit: int = 100, collection_name: str = None
):
    """Query message audit records from Firestore."""

    if collection_name is None:
        collection_name = os.environ.get(
            "FIRESTORE_AUDIT_COLLECTION", "message_audit_logs"
        )

    if filters is None:
        filters = {}

    db = firestore.Client()
    query = db.collection(collection_name)

    # Apply filters
    for field, value in filters.items():
        if isinstance(value, tuple) and len(value) == 2:
            # Handle comparison operators (field, operator, value)
            operator, op_value = value
            query = query.where(field, operator, op_value)
        else:
            query = query.where(field, "==", value)

    # Apply limit and order
    query = query.order_by("audit_timestamp", direction=firestore.Query.DESCENDING)
    query = query.limit(limit)

    try:
        results = query.stream()

        records = []
        for doc in results:
            record = doc.to_dict()
            record["_firestore_id"] = doc.id
            records.append(record)

        return {
            "success": True,
            "count": len(records),
            "records": records,
            "collection": collection_name,
            "query_filters": filters,
            "limit": limit,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "collection": collection_name,
            "query_filters": filters,
        }


def store_processing_pipeline_record(
    message_data: Any, processing_steps: Dict[str, Any], final_result: Dict[str, Any]
):
    """Store a complete message processing pipeline record."""

    # Create comprehensive audit record
    audit_record = {
        "message_id": final_result.get("message_id", "unknown"),
        "original_message": message_data
        if isinstance(message_data, (dict, list, str, int, float, bool))
        else str(message_data),
        "processing_steps": processing_steps,
        "final_result": final_result,
        "processing_timestamp": datetime.utcnow().isoformat() + "Z",
        "pipeline_version": "1.0",
        "has_translation": "translation" in processing_steps,
        "has_safety_check": "safety_check" in processing_steps,
        "was_successful": final_result.get("success", False),
        "has_dead_letter": "dead_letter_info" in final_result,
    }

    # Add step-specific metadata
    if "translation" in processing_steps:
        audit_record["translation_details"] = processing_steps["translation"].get(
            "translation_details", []
        )
        audit_record["target_language"] = processing_steps["translation"].get(
            "target_language"
        )

    if "safety_check" in processing_steps:
        audit_record["safety_result"] = processing_steps["safety_check"].get(
            "safe", True
        )
        audit_record["safety_issues"] = processing_steps["safety_check"].get(
            "safety_issues", []
        )

    # Store the record
    return store_message_audit_record(audit_record)


def search_messages_by_content(
    search_text: str,
    field: str = "original_message",
    collection_name: str = None,
    limit: int = 50,
):
    """Search for messages containing specific text (Firestore doesn't support full-text search natively)."""

    if collection_name is None:
        collection_name = os.environ.get(
            "FIRESTORE_AUDIT_COLLECTION", "message_audit_logs"
        )

    db = firestore.Client()

    # Note: Firestore doesn't support full-text search natively.
    # This is a simplified approach that works for exact matches or contains in strings.
    # For production, consider using a dedicated search service.

    try:
        # Get all records and filter client-side (not efficient for large datasets)
        all_records = db.collection(collection_name).limit(limit).stream()

        matching_records = []
        for doc in all_records:
            record = doc.to_dict()

            # Check if the field exists and contains search text
            if field in record:
                field_value = str(record[field]).lower()
                if search_text.lower() in field_value:
                    record["_firestore_id"] = doc.id
                    matching_records.append(record)

        return {
            "success": True,
            "search_text": search_text,
            "field": field,
            "matches_found": len(matching_records),
            "matching_records": matching_records,
            "collection": collection_name,
            "note": "Client-side search performed. For large datasets, consider using a dedicated search service.",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "search_text": search_text,
            "field": field,
            "collection": collection_name,
        }


def get_processing_statistics(time_range_hours: int = 24, collection_name: str = None):
    """Get processing statistics from audit records."""

    if collection_name is None:
        collection_name = os.environ.get(
            "FIRESTORE_AUDIT_COLLECTION", "message_audit_logs"
        )

    db = firestore.Client()

    # Calculate time threshold
    from datetime import datetime, timedelta

    time_threshold = datetime.utcnow() - timedelta(hours=time_range_hours)

    try:
        # Query for recent records
        query = db.collection(collection_name).where(
            "processing_timestamp", ">=", time_threshold.isoformat() + "Z"
        )

        records = query.stream()

        stats = {
            "total_messages": 0,
            "successful_messages": 0,
            "failed_messages": 0,
            "messages_with_translation": 0,
            "messages_with_safety_check": 0,
            "messages_to_dead_letter": 0,
            "time_range_hours": time_range_hours,
            "collection": collection_name,
            "calculated_at": datetime.utcnow().isoformat() + "Z",
        }

        for doc in records:
            record = doc.to_dict()
            stats["total_messages"] += 1

            if record.get("was_successful"):
                stats["successful_messages"] += 1
            else:
                stats["failed_messages"] += 1

            if record.get("has_translation"):
                stats["messages_with_translation"] += 1

            if record.get("has_safety_check"):
                stats["messages_with_safety_check"] += 1

            if record.get("has_dead_letter"):
                stats["messages_to_dead_letter"] += 1

        # Calculate percentages
        if stats["total_messages"] > 0:
            stats["success_rate"] = (
                stats["successful_messages"] / stats["total_messages"]
            ) * 100
            stats["failure_rate"] = (
                stats["failed_messages"] / stats["total_messages"]
            ) * 100
            stats["translation_rate"] = (
                stats["messages_with_translation"] / stats["total_messages"]
            ) * 100
            stats["safety_check_rate"] = (
                stats["messages_with_safety_check"] / stats["total_messages"]
            ) * 100
            stats["dead_letter_rate"] = (
                stats["messages_to_dead_letter"] / stats["total_messages"]
            ) * 100

        return {
            "success": True,
            "statistics": stats,
            "provider": "google_cloud_firestore",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "time_range_hours": time_range_hours,
            "collection": collection_name,
        }


if __name__ == "__main__":
    # Example usage
    sample_record = {
        "message_id": "test_msg_123",
        "event_type": "user_feedback",
        "processing_result": "success",
        "processing_time_ms": 150.5,
        "additional_data": {"user_id": "user_456", "rating": 5},
    }

    # Store a record
    store_result = store_message_audit_record(sample_record)
    print(f"Stored record: {json.dumps(store_result, indent=2)}")

    # Query records
    if store_result["success"]:
        query_result = query_message_audit_records(
            {"event_type": "user_feedback"}, limit=5
        )
        print(f"Query result count: {query_result.get('count', 0)}")
