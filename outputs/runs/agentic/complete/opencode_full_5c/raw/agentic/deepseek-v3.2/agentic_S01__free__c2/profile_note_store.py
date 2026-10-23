import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def get_mongodb_client():
    """
    Get MongoDB client connection.
    """
    connection_string = os.environ.get(
        "MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/"
    )
    client = MongoClient(connection_string)
    return client


def store_onboarding_note(
    user_id: str,
    note_type: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Store onboarding notes and support metadata in MongoDB.
    """
    client = get_mongodb_client()
    db = client["user_onboarding"]
    collection = db["profile_notes"]

    note_document = {
        "user_id": user_id,
        "note_type": note_type,
        "content": content,
        "metadata": metadata or {},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    try:
        result = collection.insert_one(note_document)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise Exception(f"Failed to store note: {e}")
    finally:
        client.close()


def get_user_notes(
    user_id: str, note_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve onboarding notes for a user.
    """
    client = get_mongodb_client()
    db = client["user_onboarding"]
    collection = db["profile_notes"]

    query = {"user_id": user_id}
    if note_type:
        query["note_type"] = note_type

    try:
        notes = list(collection.find(query, {"_id": 0}))
        return notes
    except PyMongoError as e:
        raise Exception(f"Failed to retrieve notes: {e}")
    finally:
        client.close()


def update_support_metadata(user_id: str, metadata_updates: Dict[str, Any]) -> bool:
    """
    Update support metadata for a user in MongoDB.
    """
    client = get_mongodb_client()
    db = client["user_onboarding"]
    collection = db["support_metadata"]

    try:
        result = collection.update_one(
            {"user_id": user_id},
            {
                "$set": {**metadata_updates, "updated_at": datetime.utcnow()},
                "$setOnInsert": {"created_at": datetime.utcnow()},
            },
            upsert=True,
        )
        return result.modified_count > 0 or result.upserted_id is not None
    except PyMongoError as e:
        raise Exception(f"Failed to update metadata: {e}")
    finally:
        client.close()


def store_onboarding_analytics(user_id: str, analytics_data: Dict[str, Any]) -> str:
    """
    Store onboarding analytics data in MongoDB.
    """
    client = get_mongodb_client()
    db = client["user_onboarding"]
    collection = db["onboarding_analytics"]

    document = {
        "user_id": user_id,
        "analytics_data": analytics_data,
        "timestamp": datetime.utcnow(),
        "event_type": "onboarding_progress",
    }

    try:
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise Exception(f"Failed to store analytics: {e}")
    finally:
        client.close()
