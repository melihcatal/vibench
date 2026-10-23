import os
from google.cloud import firestore
from messaging_models import PubSubMessage


def store_audit(message: PubSubMessage, status: str) -> str:
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is required")
    client = firestore.Client(project=project_id)
    doc_ref = client.collection("message_audits").add(
        {
            "message_id": message.message_id,
            "payload": message.payload,
            "attributes": message.attributes,
            "publish_time": message.publish_time,
            "processing_status": status,
            "stored_at": firestore.SERVER_TIMESTAMP,
        }
    )
    return doc_ref[1].id
