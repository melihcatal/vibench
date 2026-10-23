import os
from typing import Dict, Any, Optional
from messaging_client import PubSubClient
from messaging_models import EventPayload

# Google Cloud Pub/Sub provider-identifying signal: google.cloud.pubsub_v1


def send_to_dead_letter(
    dead_letter_topic_id: str,
    original_event_data: Dict[str, Any],
    error_message: str,
    original_message_id: Optional[str] = None,
) -> str:
    """Sends a failed message to a Google Cloud Pub/Sub dead-letter topic."""
    client = PubSubClient()
    dead_letter_topic_path = client.get_topic_path(dead_letter_topic_id)

    # Create a new payload for the dead-letter message, including error details
    dead_letter_payload_data = {
        "original_event": original_event_data,
        "error": error_message,
        "original_message_id": original_message_id,
    }
    dead_letter_payload = EventPayload(
        data=dead_letter_payload_data,
        event_type="dead_letter_event",
        source="failed_processing",
        event_id=f"dead-letter-{original_message_id if original_message_id else os.urandom(8).hex()}",
    )
    data = dead_letter_payload.to_json_string().encode("utf-8")

    attributes = {
        "error_reason": "processing_failed",
        "original_topic_id": original_event_data.get("source", "unknown"),
    }
    if original_message_id:
        attributes["original_message_id"] = original_message_id

    future = client.publisher.publish(dead_letter_topic_path, data, **attributes)
    message_id = future.result()
    return message_id
