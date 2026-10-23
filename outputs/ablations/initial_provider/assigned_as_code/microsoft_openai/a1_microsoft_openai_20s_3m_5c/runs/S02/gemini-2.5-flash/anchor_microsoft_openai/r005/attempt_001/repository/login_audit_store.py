import os
from pymongo import MongoClient
from datetime import datetime

def record_login_audit_event(user_id: str, event_type: str, details: dict) -> dict:
    # Initialize MongoDB Atlas client
    # Ensure MONGODB_ATLAS_URI environment variable is set

    mongo_uri = os.environ.get("MONGODB_ATLAS_URI", "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myDatabase?retryWrites=true&w=majority")
    database_name = os.environ.get("MONGODB_DATABASE_NAME", "federated_login_audit")
    collection_name = os.environ.get("MONGODB_COLLECTION_NAME", "login_events")

    if "<username>" in mongo_uri or "<password>" in mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable must be properly configured with credentials.")

    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        event_record = {
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "event_type": event_type,
            "details": details
        }

        result = collection.insert_one(event_record)

        client.close()

        return {"status": "success", "inserted_id": str(result.inserted_id)}

    except Exception as e:
        return {"status": "error", "message": f"Failed to record audit event in MongoDB Atlas: {e}"}
