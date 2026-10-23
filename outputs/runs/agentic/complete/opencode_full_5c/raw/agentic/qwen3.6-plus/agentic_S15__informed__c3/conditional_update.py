import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from database_client import get_mongo_client, get_database_name, get_collection_name
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse


def conditional_update(
    doc_id: str,
    updates: dict,
    expected_version: int | None = None,
    condition_field: str | None = None,
    condition_value: str | None = None,
) -> ConditionalUpdateResponse:
    client = get_mongo_client()
    db_name = get_database_name()
    collection_name = get_collection_name()

    try:
        db = client[db_name]
        collection = db[collection_name]

        match_filter = {"_id": doc_id}

        if expected_version is not None:
            match_filter["version"] = expected_version

        if condition_field and condition_value is not None:
            match_filter[f"data.{condition_field}"] = condition_value

        update_operations = {"$set": updates}

        if expected_version is not None:
            update_operations["$inc"] = {"version": 1}

        update_operations["$set"]["updated_at"] = datetime.utcnow().isoformat()

        result = collection.update_one(match_filter, update_operations)

        if result.matched_count == 0:
            existing = collection.find_one({"_id": doc_id})
            if existing:
                return ConditionalUpdateResponse(
                    document_id=doc_id,
                    matched=False,
                    modified=False,
                    reason="condition_not_met",
                    current_version=existing.get("version", 0),
                )
            else:
                return ConditionalUpdateResponse(
                    document_id=doc_id,
                    matched=False,
                    modified=False,
                    reason="document_not_found",
                )

        updated_doc = collection.find_one({"_id": doc_id})
        return ConditionalUpdateResponse(
            document_id=doc_id,
            matched=True,
            modified=result.modified_count > 0,
            current_version=updated_doc.get("version", 0) if updated_doc else None,
        )
    except PyMongoError as e:
        return ConditionalUpdateResponse(
            document_id=doc_id,
            matched=False,
            modified=False,
            reason="error",
            error=str(e),
        )
    finally:
        client.close()


if __name__ == "__main__":
    response = conditional_update(
        "doc-001", {"data.status": "archived"}, expected_version=1
    )
    print(response)
