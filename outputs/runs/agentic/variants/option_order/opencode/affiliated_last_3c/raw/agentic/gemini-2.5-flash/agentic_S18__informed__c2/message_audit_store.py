import os
import datetime
from google.cloud import firestore
from typing import Dict, Any, Optional
from messaging_models import MessageProcessingResult


def persist_message_audit(processing_result: MessageProcessingResult) -> str:
    """Persists a processed message record to Google Cloud Firestore for later lookup.

    Args:
        processing_result: An instance of MessageProcessingResult containing all processing details.

    Returns:
        The ID of the created Firestore document.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    # The GOOGLE_CLOUD_PROJECT environment variable is typically inferred from credentials

    db = firestore.Client()
    collection_ref = db.collection("message_audits")

    record = processing_result.to_dict()
    record["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

    try:
        doc_ref = collection_ref.add(record)
        audit_id = doc_ref[1].id  # doc_ref is a tuple (timestamp, DocumentReference)
        print(f"Successfully persisted message audit record with ID: {audit_id}")
        return audit_id
    except Exception as e:
        print(f"Error persisting message audit record to Firestore: {e}")
        raise


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable (e.g., "your-gcp-project-id")
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to a path of your service account key file

    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    example_result = MessageProcessingResult(
        message_id="msg-abc-123",
        status="completed",
        summary="Order processed successfully, items shipped.",
        safety_score={"TOXICITY": 0.01, "SEVERE_TOXICITY": 0.001},
        translated_text="Pedido procesado con éxito, artículos enviados.",
    )

    try:
        audit_record_id = persist_message_audit(example_result)
        print(f"Audit record ID: {audit_record_id}")

        # You can optionally retrieve the record to verify
        # db = firestore.Client()
        # doc = db.collection("message_audits").document(audit_record_id).get()
        # if doc.exists:
        #     print(f"Retrieved record: {doc.to_dict()}")

    except Exception as e:
        print(f"Main execution error: {e}")
