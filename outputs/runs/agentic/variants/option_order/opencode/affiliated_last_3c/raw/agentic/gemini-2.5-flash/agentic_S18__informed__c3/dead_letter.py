import os
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import EventMessage
import json


def send_to_dead_letter_topic(
    dead_letter_topic_id: str,
    failed_message_data: Dict[str, Any],
    original_message_id: str,
):
    """
    Sends a failed message's payload to a specified dead-letter topic.
    In a real Pub/Sub setup, dead-lettering is often configured directly on the subscription.
    This function simulates manually forwarding a failed message.
    """
    client = PubSubClient()
    publisher = client.get_publisher_client()
    dead_letter_topic_path = publisher.topic_path(
        client.project_id, dead_letter_topic_id
    )

    message_payload = json.dumps(failed_message_data).encode("utf-8")
    attributes = {
        "original_message_id": original_message_id,
        "reason": "processing_failed",
    }

    future = publisher.publish(dead_letter_topic_path, message_payload, **attributes)
    dead_letter_message_id = future.result()
    print(
        f"Sent failed message (original ID: {original_message_id}) to dead-letter topic {dead_letter_topic_id} with new ID: {dead_letter_message_id}"
    )
    return dead_letter_message_id


if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Create a dead-letter topic, e.g., 'my-dead-letter-topic'
    # gcloud pubsub topics create my-dead-letter-topic

    dead_letter_topic_id = os.getenv(
        "PUBSUB_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic"
    )
    failed_data = {
        "error": "Invalid payload format",
        "original_event_data": {"corrupted": "data"},
    }
    original_msg_id = "failed-event-456"
    send_to_dead_letter_topic(dead_letter_topic_id, failed_data, original_msg_id)
