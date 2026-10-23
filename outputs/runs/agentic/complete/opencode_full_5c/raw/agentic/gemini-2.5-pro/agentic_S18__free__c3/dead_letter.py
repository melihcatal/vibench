import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def send_to_dead_letter(topic_id: str, failed_message: Message):
    """Sends a failed message to a dead-letter topic."""
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    data = json.dumps(failed_message.data).encode("utf-8")

    attributes = failed_message.attributes or {}
    attributes["original_message_id"] = failed_message.message_id
    attributes["failure_reason"] = "processing_failed"

    future = publisher.publish(topic_path, data, **attributes)
    return future.result()


if __name__ == "__main__":
    dlq_topic_id = os.environ.get("GCP_DLQ_TOPIC_ID", "default-dlq-topic")
    failed_msg = Message(
        data={"payload": "This message failed processing"},
        attributes={"source": "test-script"},
    )
    print(f"Sending failed message to DLQ: {dlq_topic_id}")
    message_id = send_to_dead_letter(dlq_topic_id, failed_msg)
    print(f"Sent message to DLQ with new ID: {message_id}")
