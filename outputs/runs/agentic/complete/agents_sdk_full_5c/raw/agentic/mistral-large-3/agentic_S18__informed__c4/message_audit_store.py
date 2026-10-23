import os
from pymongo import MongoClient
from datetime import datetime
from messaging_models import EventMessage

client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
db = client["message_audit"]
collection = db["processed_messages"]

def store_message_audit(event: EventMessage, processing_metadata: dict) -> str:
    document = {
        "message_id": event.message_id,
        "data": event.data,
        "attributes": event.attributes,
        "processed_at": datetime.utcnow(),
        "metadata": processing_metadata
    }
    result = collection.insert_one(document)
    return str(result.inserted_id)