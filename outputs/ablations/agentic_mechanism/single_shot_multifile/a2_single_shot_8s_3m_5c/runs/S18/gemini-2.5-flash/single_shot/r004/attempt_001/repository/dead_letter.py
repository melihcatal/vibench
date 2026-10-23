import os
import json
from messaging_client import PubSubClientHelper
from messaging_models import EventMessage

def send_to_dead_letter(original_event: EventMessage, error_details: str) -> str:
    client_helper = PubSubClientHelper()
    publisher = client_helper.get_publisher_client()
    dead_letter_topic_id = os.environ.get("GCP_PUBSUB_DEAD_LETTER_TOPIC_ID")
    if not dead_letter_topic_id:
        raise ValueError("GCP_PUBSUB_DEAD_LETTER_TOPIC_ID environment variable not set.")

    dead_letter_topic_path = client_helper.get_topic_path(dead_letter_topic_id)

    dead_letter_data = {
        "original_event_id": original_event['event_id'],
        "original_data": original_event['data'],
        "original_attributes": original_event.get('attributes', {}),
        "error_details": error_details,
        "dead_letter_timestamp": os.path.now().isoformat()
    }

    data_bytes = json.dumps(dead_letter_data).encode("utf-8")

    attributes = {
        "event_id": original_event['event_id'],
        "reason": "processing_failed",
        "error": error_details
    }

    future = publisher.publish(dead_letter_topic_path, data_bytes, **attributes)
    message_id = future.result()

    return message_id
