import json
import os
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def send_to_dead_letter(topic_id: str, failed_message: Message, error: str):
    """
    Publishes a failed message to a dead-letter topic in Google Cloud Pub/Sub.
    """
    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_path(topic_id)

    # Enrich the original message with error context
    dead_letter_data = {
        "original_data": failed_message.data.decode("utf-8")
        if isinstance(failed_message.data, bytes)
        else failed_message.data,
        "original_attributes": failed_message.attributes,
        "error": error,
    }

    data = json.dumps(dead_letter_data).encode("utf-8")

    future = publisher.publish(dead_letter_topic_path, data)
    print(f"Sent message to dead-letter topic {topic_id} with ID: {future.result()}")
    return future.result()


if __name__ == "__main__":
    DEAD_LETTER_TOPIC_ID = os.environ.get(
        "GCP_DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
    )

    # This simulates a message that has failed processing
    original_failed_message = Message(
        data=b'{"payload": "corrupted-data"}',
        attributes={"source": "importer-service"},
        message_id="original-message-id-123",
    )
    processing_error = "Failed to parse JSON payload."

    send_to_dead_letter(DEAD_LETTER_TOPIC_ID, original_failed_message, processing_error)
