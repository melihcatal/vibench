import os
from pymongo import MongoClient
from datetime import datetime
from messaging_models import EventMessage

client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
db = client[os.getenv("MONGODB_DATABASE", "message_audit")]
collection = db[os.getenv("MONGODB_COLLECTION", "processed_messages")]

def store_message_audit(event: EventMessage, status: str) -> str:
    record = {
        "event_id": event.event_id,
        "payload": event.payload,
        "attributes": event.attributes,
        "status": status,
        "processed_at": datetime.utcnow()
    }
    
    result = collection.insert_one(record)
    return str(result.inserted_id)