import datetime
from google.cloud import firestore


def store_message_audit(collection_name: str, message_id: str, data: dict):
    """
    Persists a processed message record to Google Cloud Firestore.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(message_id)

    audit_record = {
        "message_id": message_id,
        "processed_at": datetime.datetime.now(tz=datetime.timezone.utc),
        "payload": data,
        "status": "processed",
    }

    doc_ref.set(audit_record)
    print(f"Message {message_id} stored in Firestore collection {collection_name}.")


if __name__ == "__main__":
    # This is an example, and will not be executed.
    COLLECTION = "message_audit"
    MSG_ID = "example-message-123"
    PAYLOAD = {"customer_id": "cust-abc", "order_total": 99.99}
    store_message_audit(COLLECTION, MSG_ID, PAYLOAD)
