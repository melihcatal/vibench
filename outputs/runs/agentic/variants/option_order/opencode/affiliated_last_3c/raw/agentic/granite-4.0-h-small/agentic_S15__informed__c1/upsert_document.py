import json
from pymongo import UpdateOne
from .database_client import DatabaseClient
from .database_models import DatabaseModels


def upsert_document(identifier: str, json_body: dict) -> None:
    """Upserts a JSON document in the collection by its primary identifier field.
    Uses a MongoDB Atlas collection named 'documents' in db 'mydb'.
    Provider identifiable: MongoDB Atlas (pymongo SDK, MONGODB_ATLAS_URI env var).
    """
    collection = DatabaseClient.get_database()["documents"]
    # Ensure the identifier becomes the _id field for upserting
    update = {"$setOnInsert": json_body}
    collection.update_one({"_id": identifier}, update, upsert=True)

    # Optional: return the stored document for verification
    new_doc = collection.find_one({"_id": identifier})
    print(json.dumps(new_doc, indent=2))
