from typing import Dict, Any
import json
import os
import requests

"""Persist processed message records to Google Firestore (managed NoSQL)."""

PROJECT_ID = os.getenv("PROJECT_ID")
if not PROJECT_ID:
    raise RuntimeError("PROJECT_ID environment variable not set")

# Initialize Firestore client with Google credentials from env
from google.cloud import firestore

firestore_client = firestore.Client()
COLLECTION = "processed_messages"


def store_message_record(record: Dict[str, Any]) -> str:
    """Write a single processed message record to Firestore and return its document ID."""
    doc_ref = firestore_client.collection(COLLECTION).document()
    doc_ref.set(record)
    return doc_ref.id


# Batch store helper


def store_batch(records: List[Dict[str, Any]]) -> List[str]:
    batch = firestore_client.batch()
    ids = []
    for rec in records:
        doc_ref = firestore_client.collection(COLLECTION).document()
        batch.set(doc_ref, rec)
        ids.append(doc_ref.id)
    batch.commit()
    return ids


# No further code required
