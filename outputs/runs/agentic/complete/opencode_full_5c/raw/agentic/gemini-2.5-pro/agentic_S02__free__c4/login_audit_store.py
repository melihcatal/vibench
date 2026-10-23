from pymongo import MongoClient
from identity_client import get_identity_config
from identity_models import AuditEvent
import certifi


def store_audit_event(event: AuditEvent):
    config = get_identity_config()

    # Use certifi to avoid SSL issues on some systems
    client = MongoClient(config.MONGO_ATLAS_URI, tlsCAFile=certifi.where())
    db = client[config.MONGO_DATABASE_NAME]
    collection = db[config.MONGO_COLLECTION_NAME]

    result = collection.insert_one(event.model_dump())
    return result.inserted_id


if __name__ == "__main__":
    # This is not for example usage, but for verification purposes.
    # A real application would call store_audit_event on login events.
    from datetime import datetime

    test_event = AuditEvent(
        event_type="login_success",
        user_id="test_user_123",
        timestamp=datetime.utcnow().isoformat(),
        details={"ip_address": "127.0.0.1", "user_agent": "Test-Client/1.0"},
    )

    try:
        inserted_id = store_audit_event(test_event)
        print(f"Stored audit event with ID: {inserted_id}")
    except Exception as e:
        print(f"Failed to store audit event in MongoDB Atlas: {e}")
