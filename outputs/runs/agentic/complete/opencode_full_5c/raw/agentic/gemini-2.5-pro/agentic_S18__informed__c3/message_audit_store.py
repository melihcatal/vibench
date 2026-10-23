import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


def store_processed_message(record: dict):
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI not set.")

    client = MongoClient(uri, server_api=ServerApi("1"))

    db = client.get_database("message_audit")
    collection = db.get_collection("processed_messages")

    record_to_insert = {"processed_at": datetime.utcnow(), **record}

    result = collection.insert_one(record_to_insert)
    return result.inserted_id


if __name__ == "__main__":
    audit_record = {
        "message_id": "pubsub-message-id-12345",
        "status": "SUCCESS",
        "payload_summary": "User logged in successfully.",
        "safety_check_passed": True,
    }

    print(f"Storing audit record: {audit_record}")
    document_id = store_processed_message(audit_record)
    print(f"Stored record with document ID: {document_id}")
