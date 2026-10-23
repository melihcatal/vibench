# message_audit_store.py
# [LATER-STEP]
# Persist processed message records to Google Cloud Firestore for later lookup

import os
import json
from google.cloud import firestore
from messaging_models import deserialize_message


def store_message(message: dict):
    """Write a processed message record to Firestore collection 'audit'.

    The document ID is the message 'id' field. All fields are stored as-is.
    """
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not set")

    db = firestore.Client()
    doc_ref = db.collection("audit").document(message.get("id"))
    doc_ref.set(message)
    print(f"Persisted message {message.get('id')} to Firestore")


if __name__ == "__main__":
    # CLI helper: read a JSON file and store it
    import sys

    if len(sys.argv) != 2:
        print("Usage: python message_audit_store.py <message.json>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        msg = json.load(f)
    store_message(msg)
