"""Persist onboarding notes and support metadata in MongoDB Atlas.

Uses the PyMongo SDK to connect to MongoDB Atlas and store onboarding notes,
support metadata, and moderation history as documents in a managed NoSQL
document store collection.
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def get_mongo_client() -> MongoClient:
    """Create a PyMongo client connected to MongoDB Atlas.

    Uses the MONGODB_ATLAS_URI environment variable to connect to a
    MongoDB Atlas cluster.

    Returns:
        pymongo.MongoClient instance connected to MongoDB Atlas.

    Raises:
        EnvironmentError: If MONGODB_ATLAS_URI is not set.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise EnvironmentError(
            "MONGODB_ATLAS_URI environment variable is required for MongoDB Atlas"
        )
    return MongoClient(uri)


def get_onboarding_collection(
    database_name: str = "user_onboarding",
    collection_name: str = "onboarding_notes",
) -> Collection:
    """Get the MongoDB Atlas collection for onboarding notes.

    Args:
        database_name: MongoDB database name.
        collection_name: Collection name for onboarding notes.

    Returns:
        pymongo.collection.Collection instance.
    """
    client = get_mongo_client()
    db: Database = client[database_name]
    return db[collection_name]


def store_onboarding_note(
    user_uid: str,
    note: str,
    note_type: str = "support",
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Persist an onboarding note in MongoDB Atlas.

    Creates a new document in the onboarding_notes collection with the
    user's UID, the note content, type, and any associated metadata.

    Args:
        user_uid: The unique user identifier (Firebase uid or similar).
        note: The text of the onboarding note.
        note_type: Category of note (e.g., 'support', 'moderation', 'translation').
        metadata: Optional dictionary of additional context.

    Returns:
        The inserted document's ObjectId as a string.
    """
    collection = get_onboarding_collection()

    document = {
        "user_uid": user_uid,
        "note": note,
        "note_type": note_type,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_onboarding_notes(
    user_uid: str,
    note_type: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Retrieve onboarding notes for a user from MongoDB Atlas.

    Args:
        user_uid: The unique user identifier.
        note_type: Optional filter by note type.
        limit: Maximum number of notes to return.

    Returns:
        List of note documents sorted by creation date (newest first).
    """
    collection = get_onboarding_collection()

    query: Dict[str, Any] = {"user_uid": user_uid}
    if note_type:
        query["note_type"] = note_type

    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if isinstance(doc.get("updated_at"), datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
        notes.append(doc)

    return notes


def update_onboarding_metadata(
    user_uid: str,
    metadata_key: str,
    metadata_value: Any,
) -> int:
    """Update or add a metadata key on all onboarding notes for a user.

    Args:
        user_uid: The unique user identifier.
        metadata_key: The metadata field name to update.
        metadata_value: The value to set.

    Returns:
        Number of documents modified.
    """
    collection = get_onboarding_collection()

    result = collection.update_many(
        {"user_uid": user_uid},
        {
            "$set": {
                f"metadata.{metadata_key}": metadata_value,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    return result.modified_count


def store_moderation_record(
    user_uid: str,
    moderation_result: Dict[str, Any],
    content_type: str = "profile_bio",
) -> str:
    """Store a content moderation result in MongoDB Atlas.

    Args:
        user_uid: The unique user identifier.
        moderation_result: Dict with moderation analysis results
            (is_safe, categories, flagged_categories, etc.).
        content_type: Type of content moderated (e.g., 'profile_bio', 'display_name').

    Returns:
        The inserted document's ObjectId as a string.
    """
    collection = get_onboarding_collection()

    document = {
        "user_uid": user_uid,
        "note": f"Moderation check for {content_type}",
        "note_type": "moderation",
        "metadata": {
            "content_type": content_type,
            "moderation_result": moderation_result,
            "is_safe": moderation_result.get("is_safe", False),
            "moderation_engine": "azure_content_safety",
        },
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def store_translation_record(
    user_uid: str,
    source_lang: str,
    target_lang: str,
    translated_fields: Dict[str, str],
) -> str:
    """Store a translation completion record in MongoDB Atlas.

    Args:
        user_uid: The unique user identifier.
        source_lang: Source language code.
        target_lang: Target language code.
        translated_fields: Dict of field names to translated text.

    Returns:
        The inserted document's ObjectId as a string.
    """
    collection = get_onboarding_collection()

    document = {
        "user_uid": user_uid,
        "note": f"Onboarding translation: {source_lang} -> {target_lang}",
        "note_type": "translation",
        "metadata": {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "translated_fields": list(translated_fields.keys()),
            "translation_engine": "deepl",
        },
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)
