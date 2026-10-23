from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

def profile_note_store(user_id, notes, metadata):
    # Replace the placeholder with your Atlas connection string
    uri = os.environ.get("MONGODB_ATLAS_URI")

    # Set the Stable API version when creating a new MongoClient
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        db = client.get_database("onboarding_db")
        notes_collection = db.get_collection("profile_notes")

        note_document = {
            "user_id": user_id,
            "notes": notes,
            "metadata": metadata,
            "timestamp": os.environ.get("CURRENT_TIMESTAMP") # Placeholder for a real timestamp
        }

        result = notes_collection.insert_one(note_document)
        return str(result.inserted_id)

    except Exception as e:
        raise RuntimeError(f"MongoDB Atlas operation failed: {e}")
    finally:
        client.close()
