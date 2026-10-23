import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from identity_models import ProfileNoteStoreRequest, ProfileNoteStoreResponse

MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    raise EnvironmentError("MONGODB_URI environment variable not set.")

# Database and collection names
DB_NAME = "onboarding"
COLLECTION_NAME = "profile_notes"

def store_profile_notes(request: ProfileNoteStoreRequest) -> ProfileNoteStoreResponse:
    client = None
    try:
        client = MongoClient(MONGODB_URI)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster') 
        
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        document = {
            "user_id": request.user_id,
            "notes": request.notes,
            "metadata": request.metadata,
            "timestamp": datetime.datetime.utcnow()
        }

        result = collection.insert_one(document)
        return ProfileNoteStoreResponse(inserted_id=str(result.inserted_id))
    except ConnectionFailure as e:
        raise ConnectionError(f"MongoDB connection failed: {e}")
    except Exception as e:
        raise ValueError(f"Failed to store profile notes in MongoDB: {e}")
    finally:
        if client:
            client.close()

import datetime # Moved import to top for cleaner code after refactoring