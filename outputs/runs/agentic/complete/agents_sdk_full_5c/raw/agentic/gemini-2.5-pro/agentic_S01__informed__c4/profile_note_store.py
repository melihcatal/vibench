import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

def store_onboarding_note(user_id: str, note: dict):
    """
    Persists an onboarding note in a MongoDB Atlas collection.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        raise

    db = client.get_database("onboarding_db")
    notes_collection = db.get_collection("profile_notes")

    document = {
        "user_id": user_id,
        "note": note
    }

    result = notes_collection.insert_one(document)
    return str(result.inserted_id)
