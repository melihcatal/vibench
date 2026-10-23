from datetime import datetime, timezone

from identity_client import (
    mongodb_client,
    mongodb_collection_name,
    mongodb_database_name,
)
from identity_models import ProfileNoteStoreRequest, normalize_note_record


def profile_note_store(request: ProfileNoteStoreRequest):
    client = mongodb_client()
    collection = client[mongodb_database_name()][mongodb_collection_name()]
    document = {
        "user_id": request.user_id,
        "email": request.email,
        "notes": request.notes,
        "support_metadata": request.support_metadata,
        "provider": "mongodb-atlas",
        "updated_at": datetime.now(timezone.utc),
    }
    result = collection.update_one(
        {"user_id": request.user_id}, {"$set": document}, upsert=True
    )
    stored = dict(document)
    stored["matched_count"] = result.matched_count
    stored["modified_count"] = result.modified_count
    stored["upserted_id"] = (
        str(result.upserted_id) if result.upserted_id is not None else None
    )
    document_id = stored["upserted_id"] or request.user_id
    return normalize_note_record(document_id, stored)
