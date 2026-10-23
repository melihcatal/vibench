"""
Persist onboarding notes and support metadata in MongoDB Atlas.

Uses MongoDB Atlas service (pymongo SDK).
Auth: MONGODB_ATLAS_URI
Provider: MongoDB Atlas (atlas.mongodb.com)
"""

import os
from typing import Optional, Dict, List, Any
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.collection import Collection
from pymongo.database import Database


DEFAULT_DATABASE_NAME = "identity_platform"
DEFAULT_NOTES_COLLECTION = "onboarding_notes"
DEFAULT_METADATA_COLLECTION = "support_metadata"


class ProfileNoteStore:
    """Handles persistence of onboarding notes and support metadata in MongoDB Atlas."""

    def __init__(
        self,
        uri: Optional[str] = None,
        database_name: str = DEFAULT_DATABASE_NAME,
        notes_collection: str = DEFAULT_NOTES_COLLECTION,
        metadata_collection: str = DEFAULT_METADATA_COLLECTION,
    ):
        self.uri = uri or os.getenv("MONGODB_ATLAS_URI", "")
        self.client = MongoClient(self.uri)
        self.database: Database = self.client[database_name]
        self.notes_collection: Collection = self.database[notes_collection]
        self.metadata_collection: Collection = self.database[metadata_collection]

        # Ensure indexes for efficient lookups
        self.notes_collection.create_index("user_id")
        self.notes_collection.create_index("created_at")
        self.metadata_collection.create_index("user_id")

    def add_onboarding_note(
        self,
        user_id: str,
        note_text: str,
        category: str = "onboarding",
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Add an onboarding note for a user to MongoDB Atlas.

        Args:
            user_id: The user's unique identifier.
            note_text: The content of the note.
            category: Categorization of the note (e.g., 'onboarding', 'support', 'moderation').
            author: Optional identifier of the note author.
            tags: Optional list of tags for the note.

        Returns:
            The MongoDB document ID of the inserted note.
        """
        now = datetime.now(timezone.utc)
        note_doc = {
            "user_id": user_id,
            "note_text": note_text,
            "category": category,
            "author": author or "system",
            "tags": tags or [],
            "created_at": now,
            "updated_at": now,
        }

        result = self.notes_collection.insert_one(note_doc)
        return str(result.inserted_id)

    def get_user_notes(
        self,
        user_id: str,
        category: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all onboarding notes for a user from MongoDB Atlas.
        """
        query: Dict[str, Any] = {"user_id": user_id}
        if category:
            query["category"] = category

        cursor = self.notes_collection.find(query).sort("created_at", -1).limit(limit)
        notes = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            if isinstance(doc.get("created_at"), datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            if isinstance(doc.get("updated_at"), datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            notes.append(doc)

        return notes

    def update_note(
        self,
        note_id: str,
        updated_text: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """
        Update an existing onboarding note in MongoDB Atlas.
        """
        from bson import ObjectId
        updates: Dict[str, Any] = {"updated_at": datetime.now(timezone.utc)}
        if updated_text is not None:
            updates["note_text"] = updated_text
        if tags is not None:
            updates["tags"] = tags

        result = self.notes_collection.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": updates},
        )
        return result.modified_count > 0

    def store_support_metadata(
        self,
        user_id: str,
        metadata: Dict[str, Any],
    ) -> str:
        """
        Store or upsert support metadata for a user in MongoDB Atlas.
        """
        now = datetime.now(timezone.utc)
        metadata_doc = {
            "user_id": user_id,
            "metadata": metadata,
            "updated_at": now,
        }

        result = self.metadata_collection.update_one(
            {"user_id": user_id},
            {
                "$set": metadata_doc,
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )

        return str(result.upserted_id) if result.upserted_id else "updated"

    def get_support_metadata(
        self,
        user_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve support metadata for a user from MongoDB Atlas.
        """
        doc = self.metadata_collection.find_one({"user_id": user_id})
        if doc:
            doc["_id"] = str(doc["_id"])
            if isinstance(doc.get("created_at"), datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            if isinstance(doc.get("updated_at"), datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
        return doc

    def store_full_onboarding_record(
        self,
        user_id: str,
        onboarding_data: Dict[str, Any],
        notes: Optional[List[str]] = None,
        support_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """
        Store a complete onboarding record including notes and metadata.

        Args:
            user_id: The user's unique identifier.
            onboarding_data: Full onboarding state dictionary.
            notes: Optional list of note strings to add.
            support_metadata: Optional support metadata to store.

        Returns:
            Dict with IDs of created documents.
        """
        results: Dict[str, str] = {}

        # Store onboarding notes
        if notes:
            note_ids = []
            for note in notes:
                note_id = self.add_onboarding_note(user_id, note, category="onboarding")
                note_ids.append(note_id)
            results["note_ids"] = ", ".join(note_ids)

        # Store the main onboarding data as a note
        import json
        data_note_id = self.add_onboarding_note(
            user_id,
            json.dumps(onboarding_data, default=str),
            category="onboarding_state",
            tags=["state_snapshot"],
        )
        results["state_note_id"] = data_note_id

        # Store support metadata
        if support_metadata:
            meta_result = self.store_support_metadata(user_id, support_metadata)
            results["metadata_id"] = meta_result

        return results

    def close(self):
        """Close the MongoDB Atlas connection."""
        self.client.close()


def persist_onboarding_notes(
    user_id: str,
    onboarding_data: Dict[str, Any],
    notes: Optional[List[str]] = None,
    support_metadata: Optional[Dict[str, Any]] = None,
    uri: Optional[str] = None,
) -> Dict[str, str]:
    """
    Convenience function to persist onboarding notes and metadata to MongoDB Atlas.
    """
    store = ProfileNoteStore(uri=uri)
    try:
        return store.store_full_onboarding_record(
            user_id=user_id,
            onboarding_data=onboarding_data,
            notes=notes,
            support_metadata=support_metadata,
        )
    finally:
        store.close()
