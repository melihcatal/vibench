import json
from datetime import datetime
from typing import Dict, Any

# Azure Service Bus client utilities from helper
from .messaging_client import get_client


def store_processed_record(record: Dict[str, Any]) -> None:
    """Persist a processed message record to a managed NoSQL document store (MongoDB Atlas)."""
    MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
    if not MONGO_URI:
        raise RuntimeError(
            "Set MONGODB_ATLAS_URI environment variable to enable persistence"
        )
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    collection = db.processed_messages
    # Add audit fields
    audit = {
        "ingested_at": datetime.utcnow().isoformat(),
        "source": "pubsub-processing",
    }
    # Merge audit into the record
    record = {**record, **audit}
    collection.insert_one(record)


# Example workflow:
# raw = consume_event(\"my-sub\")
# processed = enrich_and_validate(raw)
# store_processed_record(processed)
