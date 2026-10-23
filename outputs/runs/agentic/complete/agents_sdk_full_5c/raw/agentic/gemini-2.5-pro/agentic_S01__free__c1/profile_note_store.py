import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime

load_dotenv()

def get_mongo_client():
    """Initializes and returns a MongoDB client connected to Atlas."""
    uri = os.environ.get("MONGO_ATLAS_URI")
    if not uri:
        raise ValueError("MONGO_ATLAS_URI environment variable must be set.")
    
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}")
        raise
    return client

try:
    client = get_mongo_client()
    db = client.get_database("user_profiles")
    notes_collection = db.get_collection("onboarding_notes")
except (ValueError, Exception) as e:
    print(f"MongoDB client could not be initialized: {e}")
    client = None
    notes_collection = None


def save_onboarding_note(user_id: str, note_content: str, support_agent: str) -> str:
    """
    Saves an onboarding note to MongoDB Atlas for a given user.
    Returns the ID of the newly created note.
    """
    if not notes_collection:
        raise ConnectionError("MongoDB notes collection is not available.")

    document = {
        "user_id": user_id,
        "note": note_content,
        "agent": support_agent,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    result = notes_collection.insert_one(document)
    return str(result.inserted_id)
