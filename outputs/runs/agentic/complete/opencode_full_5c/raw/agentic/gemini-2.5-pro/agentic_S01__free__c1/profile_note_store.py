import os
from pymongo import MongoClient
from identity_models import ProfileData


def store_profile_notes(profile_data: ProfileData) -> dict:
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        return {"error": "MONGODB_ATLAS_URI environment variable not set."}

    client = MongoClient(connection_string)
    db = client.get_database("user_profiles")
    collection = db.get_collection("onboarding_notes")

    document = {
        "user_id": profile_data.user_id,
        "profile_text": profile_data.profile_text,
        "notes": profile_data.notes,
    }

    try:
        result = collection.insert_one(document)
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        client.close()
