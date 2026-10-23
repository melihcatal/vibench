import os
import datetime
from typing import Dict, Any, Optional
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ConnectionFailure, OperationFailure

class LoginAuditStore:
    def __init__(self):
        """
        Initializes the connection to a MongoDB Atlas database.
        """
        mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")
        
        try:
            self.client = MongoClient(mongo_uri)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
        except ConnectionFailure as e:
            raise RuntimeError(f"Could not connect to MongoDB Atlas: {e}") from e
            
        self.db = self.client.get_database("federated_logins")
        self.collection = self.db.get_collection("audit_events")

    def record_login_event(self, event_data: Dict[str, Any]) -> str:
        """
        Persists a new federated login audit event to MongoDB Atlas.

        Args:
            event_data: A dictionary containing details of the login event.

        Returns:
            The unique ID of the inserted document.
        """
        if 'timestamp' not in event_data:
            event_data['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
        
        try:
            result = self.collection.insert_one(event_data)
            return str(result.inserted_id)
        except OperationFailure as e:
            # Handle potential errors like write conflicts, schema validation, etc.
            raise IOError(f"Failed to insert audit event into MongoDB: {e}") from e

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific audit event by its document ID.
        
        Note: MongoDB IDs are typically ObjectId, but we search by string representation.
        """
        from bson.objectid import ObjectId, InvalidId
        try:
            doc_id = ObjectId(event_id)
        except InvalidId:
            return None
            
        return self.collection.find_one({"_id": doc_id})

    def find_events_by_subject(self, subject_id: str) -> list[Dict[str, Any]]:
        """
        Finds all audit events for a given user subject ID.
        """
        cursor = self.collection.find({"user.subject": subject_id}).sort("timestamp", -1)
        return list(cursor)

    def close_connection(self):
        """Closes the MongoDB client connection."""
        self.client.close()
