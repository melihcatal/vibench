from google.cloud import firestore
import os
from typing import Dict, Optional
from datetime import datetime

# Initialize Firestore client
firestore_client = firestore.Client()


def message_audit_store(message_data: Dict, status: str) -> str:
    """
    Persists processed message records to Google Cloud Firestore for later lookup.

    Args:
        message_data: Dictionary containing message data.
        status: Processing status of the message (e.g., 'processed', 'failed').

    Returns:
        str: The document ID of the stored message record.
    """
    # Add metadata to the message
    audit_record = {
        "message_id": message_data.get("message_id", ""),
        "content": message_data.get("content", ""),
        "status": status,
        "timestamp": datetime.utcnow(),
        "metadata": message_data.get("metadata", {}),
    }

    # Add the record to Firestore
    doc_ref = firestore_client.collection("message_audit").add(audit_record)

    return doc_ref[1].id
