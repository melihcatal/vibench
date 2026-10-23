import os
import json

from messaging_client import get_publisher_client, get_topic_path
from messaging_models import ReceivedMessage

def send_to_dead_letter_queue(message: ReceivedMessage, reason: str):
    """
    Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub.

    Args:
        message: The original message that failed processing.
        reason: A string explaining why the message failed.
    """
    dlq_topic_id = os.getenv("GCP_PUBSUB_DLQ_TOPIC_ID")
    if not dlq_topic_id:
        raise ValueError("GCP_PUBSUB_DLQ_TOPIC_ID environment variable not set.")

    publisher_client = get_publisher_client()
    topic_path = get_topic_path(publisher_client, dlq_topic_id)

    # Add failure reason to the message attributes
    attributes = message.attributes.copy()
    attributes["deadLetterReason"] = reason
    attributes["original_ack_id"] = message.ack_id

    future = publisher_client.publish(
        topic_path, message.data, **attributes
    )

    message_id = future.result()
    print(f"Message {message_id} sent to dead-letter topic {topic_path} due to: {reason}")
    return message_id

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    # To run, set GCP_PROJECT_ID and GCP_PUBSUB_DLQ_TOPIC_ID environment variables.
    sample_failed_message = ReceivedMessage(
        ack_id="sample_ack_id_123",
        data=json.dumps({"payload": "some invalid data"}).encode('utf-8'),
        attributes={"source": "original_topic"}
    )
    try:
        send_to_dead_letter_queue(sample_failed_message, "JSONDecodeError")
    except ValueError as e:
        print(e)
