import os
from datetime import datetime
from pymongo import MongoClient
from messaging_models import ProcessedRecord


def store_processed_message(record: ProcessedRecord):
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["messaging_db"]
    collection = db["audit_records"]
    record.processing_timestamp = datetime.utcnow().isoformat()
    result = collection.insert_one(record.model_dump())
    print(f"Stored with ID: {result.inserted_id}")


if __name__ == "__main__":
    record = ProcessedRecord(
        event_id="audit-001",
        original_message="Sample processed message",
        summary="Summary of processing",
        safety_score=0.12,
        translated_message="Mensaje procesado",
    )
    store_processed_message(record)
