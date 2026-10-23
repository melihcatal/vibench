from google.cloud import firestore
from typing import Dict, Any
from messaging_models import PubSubMessage
from messaging_client import get_project_id
import datetime


def persist_processed_message(
    message: PubSubMessage, processing_results: Dict[str, Any]
) -> str:
    """Persists a processed message record to Google Cloud Firestore.

    Args:
        message: The PubSubMessage object that was processed.
        processing_results: A dictionary containing the results of the message processing.

    Returns:
        The ID of the document created in Firestore.
    """
    db = firestore.Client(project=get_project_id())

    # Reference to a collection (e.g., 'processed_messages')
    collection_ref = db.collection("processed_messages")

    record = {
        "message_id": message.message_id,
        "original_data": message.data,
        "original_attributes": message.attributes,
        "processing_results": processing_results,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    # Add a new document to the collection. Firestore will auto-generate a document ID.
    doc_ref = collection_ref.add(record)

    return doc_ref[1].id  # doc_ref is a tuple (update_time, DocumentReference)
