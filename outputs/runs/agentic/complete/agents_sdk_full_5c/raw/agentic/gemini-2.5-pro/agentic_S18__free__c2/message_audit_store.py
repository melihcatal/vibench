import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

from messaging_models import ProcessedMessage

def store_message_audit(processed_message: ProcessedMessage):
    """
    Persists a processed message record for audit purposes in MongoDB Atlas.
    """
    connection_string = os.getenv("MONGO_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGO_ATLAS_CONNECTION_STRING not set.")

    try:
        client = MongoClient(connection_string)
        db = client.get_database("message_audits")
        collection = db.get_collection("processed_messages")

        audit_record = {
            "message_id": processed_message.message_id,
            "original_payload": processed_message.original_payload,
            "status": processed_message.status,
            "is_safe": processed_message.is_safe,
            "translation_output": processed_message.translation,
            "summary_output": processed_message.summary,
            "processed_at": datetime.utcnow()
        }
        
        result = collection.insert_one(audit_record)
        print(f"Stored audit record with ID: {result.inserted_id}")
        return result.inserted_id
        
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while storing audit record: {e}")
        return None
