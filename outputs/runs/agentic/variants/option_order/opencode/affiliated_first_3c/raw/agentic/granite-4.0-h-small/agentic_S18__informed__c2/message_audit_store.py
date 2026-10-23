import json
from datetime import datetime
from ibm_cloudant.document import Document
from ibm_cloudant.client import Cloudant
from messaging_client import get_client


def audit_message(
    raw_message: Dict[str, Any], status: str, processing_time: Optional[str] = None
):
    """Persist a processed message record in IBM Cloudant for later lookup.

    Parameters:
        raw_message (dict): The original JSON payload received from the
            subscription.
        status (str): Processing outcome - "success" or "failure".
        processing_time (str, optional): ISO timestamp when processing completed.
    """
    if not processing_time:
        processing_time = datetime.utcnow().isoformat() + "Z"
    # Build Cloudant document
    doc = {
        "_id": raw_message.get(
            "event_id",
            f"msg-{datetime.utcnow().isoformat().replace(' ', 'T').replace('+', 'Z')[:23]}",
        ),
        "event_id": raw_message.get("event_id"),
        "type": raw_message.get("type"),
        "timestamp": raw_message.get("timestamp"),
        "status": status,
        "processing_time": processing_time,
        "raw_payload": raw_message,
    }
    # Initialize Cloudant client using IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY
    cloudant = Cloudant.iam(
        get_client().configuration.hosts[0],  # reuse same hostname from Kafka client
        username=get_client().configuration.api_user,
        password=get_client().configuration.api_key,
    )
    # Assume a database named "message_audit" exists
    db = cloudant["message_audit"]
    # Create or overwrite the document
    db.create_document(doc)
    print(f"Audited message {doc['_id']} with status {status}")


# Example usage (for local testing)
if __name__ == "__main__":
    mock = {
        "event_id": "audit-test-001",
        "type": "order_created",
        "timestamp": "2025-08-15T12:34:56Z",
        "data": {"order_number": "ORD-001", "amount": 250.0},
    }
    audit_message(mock, status="success")
