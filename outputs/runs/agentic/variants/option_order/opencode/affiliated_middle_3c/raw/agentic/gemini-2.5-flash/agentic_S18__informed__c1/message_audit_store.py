import os
import datetime
from typing import Dict, Any
from google.cloud import firestore

# Google Firestore provider-identifying signal: google.cloud.firestore


def persist_message_record(collection_name: str, message_record: Dict[str, Any]) -> str:
    """Persists processed message records for later lookup in Google Firestore."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment or configured via gcloud auth
    # No explicit API key needed if credentials are set up for the environment.

    db = firestore.Client()

    # Add a timestamp to the record
    message_record["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc)

    # Add a new document to the specified collection
    doc_ref = db.collection(collection_name).add(message_record)

    # The add() method returns a tuple; the second element is the document reference.
    doc_id = doc_ref[1].id
    return doc_id
