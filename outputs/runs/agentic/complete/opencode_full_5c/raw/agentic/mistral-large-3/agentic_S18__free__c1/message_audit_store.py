from google.cloud import firestore
import os
from typing import Dict, Any, Optional

# Initialize Firestore client
firestore_client = firestore.Client()


def message_audit_store(message_data: Dict[str, Any], status: str) -> str:
    """
    Persists processed message records to Google Cloud Firestore for later lookup.

    Args:
        message_data: The message data to store.
        status: The processing status of the message (e.g., 'processed', 'failed').

    Returns:
        str: The document ID of the stored message record.
    """
    # Add metadata to the message data
    message_record = {
        **message_data,
        "status": status,
        "timestamp": firestore.SERVER_TIMESTAMP,
    }

    # Add the message to the 'processed_messages' collection
    doc_ref = firestore_client.collection("processed_messages").add(message_record)

    return doc_ref[1].id
