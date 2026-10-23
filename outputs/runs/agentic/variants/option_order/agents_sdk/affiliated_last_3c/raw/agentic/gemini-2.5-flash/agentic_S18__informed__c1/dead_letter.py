import os
import json
from typing import Dict, Any
from messaging_client import get_pubsub_publisher_client
from messaging_models import EventMessage, PublishResponse

def send_to_dead_letter(dead_letter_topic_id: str, original_message: Dict[str, Any], error_details: str) -> PublishResponse:
    """Sends a failed message to a Google Cloud Pub/Sub dead-letter topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_pubsub_publisher_client()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Wrap original message and error details in a new payload for the dead-letter topic
    dlq_payload = {
        "original_message": original_message,
        "error_details": error_details,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    from datetime import datetime

    # Convert payload to bytes
    data = json.dumps(dlq_payload).encode("utf-8")
    
    attributes = {
        "original_message_id": original_message.get("message_id", "unknown"),
        "error_type": "processing_failure"
    }

    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    message_id = future.result()

    return PublishResponse(message_id=message_id)
