import json
from typing import Any
from google.cloud import firestore
from messaging_models import ConsumeResponse


def store_processed(message: ConsumeResponse) -> str:
    """Persist a processed message record to Google Firestore for later lookup.

    Returns the generated document ID.
    """
    db = firestore.Client()
    collection = db.collection("processed_messages")
    doc = collection.add(
        {
            "event_id": message.get("message_id")
            or json.dumps(message.get("payload")).split('"')[1],
            "timestamp": json.dumps(message.get("timestamp")),
            "payload": message.get("payload"),
            "status": message.get("status"),
        }
    )
    print(f"Stored processed message in Firestore doc ID {doc.id}")
    return doc.id
