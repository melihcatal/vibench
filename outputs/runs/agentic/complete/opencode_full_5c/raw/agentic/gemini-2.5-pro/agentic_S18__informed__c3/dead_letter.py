import os
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def send_to_dead_letter_queue(failed_message: Message):
    publisher = get_publisher_client()
    dead_letter_topic_id = os.environ.get(
        "GCP_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic"
    )
    topic_path = get_topic_path(dead_letter_topic_id)

    # Add reason for failure to attributes if not present
    if not failed_message.attributes:
        failed_message.attributes = {}

    failed_message.attributes["failure_reason"] = "processing_failed"

    future = publisher.publish(
        topic_path, failed_message.to_json(), **failed_message.attributes
    )
    return future.result()


if __name__ == "__main__":
    # This is a placeholder for a message that failed processing
    failed_msg = Message(
        data={"payload": "invalid_data"}, attributes={"source": "test_script"}
    )
    print(f"Sending failed message to dead-letter queue: {failed_msg.data}")
    message_id = send_to_dead_letter_queue(failed_msg)
    print(f"Sent message with ID: {message_id}")
