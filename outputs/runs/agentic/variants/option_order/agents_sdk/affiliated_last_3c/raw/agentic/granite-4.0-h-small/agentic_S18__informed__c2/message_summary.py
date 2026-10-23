import os
import json
from typing import List, Dict
from google.cloud import firestore

from messaging_models import MessageRecord, EventPayload

# Firestore credentials are provided via GOOGLE_APPLICATION_CREDENTIALS
firestore_client = None

def _init_firestore() -> None:
    """Lazily initialize a Firestore client if not already created."""
    global firestore_client
    if firestore_client is None:
        from google.cloud import firestore
        firestore_client = firestore.Client()

def persist_summary(batch_id: str, records: List[MessageRecord]) -> None:
    """Persist a summary of processed messages for the given batch.

    The summary is stored as a document in Firestore under collection
    `batch_summaries`. Each document contains:
      - batch_id (string)
      - processed_at (timestamp)
      - total_messages (int)
      - successes (int)
      - failures (int)
      - error_details (list of str, optional)
    """
    _init_firestore()
    summary = {
        "batch_id": batch_id,
        "processed_at": firestore.SERVER_TIMESTAMP,
        "total_messages": len(records),
        "successes": sum(1 for r in records if r["status"] == "processed"),
        "failures": sum(1 for r in records if r.get("error")),
    }
    # Store error details only if there are any failures
    if any(r.get("error") for r in records):
        error_details = [r["error"] for r in records if r.get("error")]
        summary["error_details"] = error_details
    doc_ref = firestore_client.collection("batch_summaries").document(batch_id)
    doc_ref.set(summary)
    print(f"Batch summary stored for {batch_id}")


def get_summary(batch_id: str) -> Dict:
    """Retrieve a previously stored batch summary.

    Returns an empty dict if the batch record does not exist.
    """
    _init_firestore()
    doc_ref = firestore_client.collection("batch_summaries").document(batch_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {}


def get_latest_summaries(limit: int = 10) -> List[Dict]:
    """Fetch the most recent `limit` batch summaries ordered by processed_at descending."""
    _init_firestore()
    query = (
        firestore_client.collection("batch_summaries")
        .order_by("processed_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    return [doc.to_dict() for doc in query.stream()]
