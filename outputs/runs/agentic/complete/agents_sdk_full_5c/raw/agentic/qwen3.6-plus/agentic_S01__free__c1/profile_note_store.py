"""
Persist onboarding notes and support metadata in MongoDB Atlas.
Provider: MongoDB Atlas (pymongo with mongodb+srv:// connection)
"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure, OperationFailure


MONGODB_ATLAS_CLUSTER_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/"
)
DEFAULT_DATABASE = "identity_lifecycle"
DEFAULT_NOTES_COLLECTION = "profile_notes"
DEFAULT_SUPPORT_COLLECTION = "support_metadata"


class ProfileNoteStore:
    """Persist onboarding notes and support metadata in MongoDB Atlas."""

    def __init__(
        self,
        uri: Optional[str] = None,
        database: Optional[str] = None,
        notes_collection: Optional[str] = None,
        support_collection: Optional[str] = None,
    ):
        self.uri = uri or MONGODB_ATLAS_CLUSTER_URI
        self.database_name = database or DEFAULT_DATABASE
        self.notes_collection_name = notes_collection or DEFAULT_NOTES_COLLECTION
        self.support_collection_name = support_collection or DEFAULT_SUPPORT_COLLECTION
        self._client: Optional[MongoClient] = None
        self._db = None

    def _get_client(self) -> MongoClient:
        """Get or create MongoDB client connection."""
        if self._client is None:
            self._client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
        return self._client

    def _get_database(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = self._get_client()[self.database_name]
        return self._db

    def _get_notes_collection(self):
        """Get the profile notes collection."""
        return self._get_database()[self.notes_collection_name]

    def _get_support_collection(self):
        """Get the support metadata collection."""
        return self._get_database()[self.support_collection_name]

    def close(self):
        """Close the MongoDB client connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def store_onboarding_note(
        self,
        user_id: str,
        note: str,
        note_type: str = "onboarding",
        created_by: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Store an onboarding note for a user in MongoDB Atlas.

        Args:
            user_id: The user's unique identifier
            note: The note content
            note_type: Type of note (onboarding, support, moderation, etc.)
            created_by: User/system that created the note
            metadata: Optional additional metadata dict

        Returns:
            Dict with storage result including inserted document ID
        """
        document = {
            "user_id": user_id,
            "note": note,
            "note_type": note_type,
            "created_by": created_by or "system",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "metadata": metadata or {},
            "provider": "mongodb_atlas",
            "database": self.database_name,
            "collection": self.notes_collection_name,
        }

        try:
            collection = self._get_notes_collection()
            result = collection.insert_one(document)

            return {
                "success": True,
                "document_id": str(result.inserted_id),
                "user_id": user_id,
                "note_type": note_type,
                "provider": "mongodb_atlas",
                "database": self.database_name,
                "collection": self.notes_collection_name,
            }

        except PyMongoError as exc:
            return {
                "success": False,
                "user_id": user_id,
                "note_type": note_type,
                "provider": "mongodb_atlas",
                "error": str(exc),
            }

    def store_support_metadata(
        self,
        user_id: str,
        ticket_id: Optional[str] = None,
        status: str = "open",
        onboarding_state: Optional[Dict[str, Any]] = None,
        moderation_result: Optional[Dict[str, Any]] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Store support metadata for a user in MongoDB Atlas.

        Args:
            user_id: The user's unique identifier
            ticket_id: Optional support ticket reference
            status: Support case status
            onboarding_state: Dict with onboarding progress
            moderation_result: Dict with moderation results
            notes: Optional support notes

        Returns:
            Dict with storage result
        """
        document = {
            "user_id": user_id,
            "ticket_id": ticket_id,
            "status": status,
            "onboarding_state": onboarding_state or {},
            "moderation_result": moderation_result or {},
            "notes": notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "provider": "mongodb_atlas",
            "database": self.database_name,
            "collection": self.support_collection_name,
        }

        try:
            collection = self._get_support_collection()
            result = collection.insert_one(document)

            return {
                "success": True,
                "document_id": str(result.inserted_id),
                "user_id": user_id,
                "ticket_id": ticket_id,
                "provider": "mongodb_atlas",
                "database": self.database_name,
                "collection": self.support_collection_name,
            }

        except PyMongoError as exc:
            return {
                "success": False,
                "user_id": user_id,
                "provider": "mongodb_atlas",
                "error": str(exc),
            }

    def get_user_notes(
        self,
        user_id: str,
        note_type: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Retrieve notes for a user from MongoDB Atlas.

        Args:
            user_id: The user's unique identifier
            note_type: Optional filter by note type
            limit: Maximum number of notes to return

        Returns:
            Dict with notes list and metadata
        """
        query = {"user_id": user_id}
        if note_type:
            query["note_type"] = note_type

        try:
            collection = self._get_notes_collection()
            cursor = collection.find(query).sort("created_at", -1).limit(limit)

            notes = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                if "created_at" in doc and isinstance(doc["created_at"], datetime):
                    doc["created_at"] = doc["created_at"].isoformat() + "Z"
                if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                    doc["updated_at"] = doc["updated_at"].isoformat() + "Z"
                notes.append(doc)

            return {
                "success": True,
                "user_id": user_id,
                "notes": notes,
                "count": len(notes),
                "provider": "mongodb_atlas",
                "database": self.database_name,
                "collection": self.notes_collection_name,
            }

        except PyMongoError as exc:
            return {
                "success": False,
                "user_id": user_id,
                "provider": "mongodb_atlas",
                "error": str(exc),
            }

    def get_support_case(
        self,
        user_id: str,
    ) -> Dict[str, Any]:
        """
        Retrieve the most recent support case for a user.

        Args:
            user_id: The user's unique identifier

        Returns:
            Dict with support case data
        """
        try:
            collection = self._get_support_collection()
            doc = collection.find_one({"user_id": user_id}, sort=[("created_at", -1)])

            if doc is None:
                return {
                    "success": True,
                    "user_id": user_id,
                    "case": None,
                    "provider": "mongodb_atlas",
                }

            doc["_id"] = str(doc["_id"])
            for date_field in ["created_at", "updated_at"]:
                if date_field in doc and isinstance(doc[date_field], datetime):
                    doc[date_field] = doc[date_field].isoformat() + "Z"

            return {
                "success": True,
                "user_id": user_id,
                "case": doc,
                "provider": "mongodb_atlas",
                "database": self.database_name,
                "collection": self.support_collection_name,
            }

        except PyMongoError as exc:
            return {
                "success": False,
                "user_id": user_id,
                "provider": "mongodb_atlas",
                "error": str(exc),
            }

    def verify_connection(self) -> Dict[str, Any]:
        """Verify connection to MongoDB Atlas cluster."""
        try:
            client = self._get_client()
            client.admin.command("ping")
            return {
                "success": True,
                "provider": "mongodb_atlas",
                "uri": self.uri[:20] + "..." if len(self.uri) > 20 else self.uri,
                "database": self.database_name,
            }
        except ConnectionFailure as exc:
            return {
                "success": False,
                "provider": "mongodb_atlas",
                "error": f"Connection failed: {str(exc)}",
            }
        except OperationFailure as exc:
            return {
                "success": False,
                "provider": "mongodb_atlas",
                "error": f"Authentication failed: {str(exc)}",
            }


if __name__ == "__main__":
    store = ProfileNoteStore()
    conn_result = store.verify_connection()
    print(f"MongoDB Atlas connection: {conn_result}")
    store.close()
