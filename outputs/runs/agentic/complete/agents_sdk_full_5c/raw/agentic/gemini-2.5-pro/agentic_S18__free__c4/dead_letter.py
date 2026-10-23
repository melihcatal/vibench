import os
from typing import Union
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path


def send_to_dead_letter_queue(
    dead_letter_topic_id: str,
    failed_message_data: Union[str, bytes],
    attributes: dict,
):
    """
    Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub.

    Args:
        dead_letter_topic_id: The ID of the dead-letter topic.
        failed_message_data: The data of the message that failed processing.
        attributes: Metadata about the failure, e.g., error reason.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(dead_letter_topic_id)

    if isinstance(failed_message_data, str):
        data = failed_message_data.encode("utf-8")
    else:
        data = failed_message_data

    future = publisher.publish(topic_path, data, **attributes)
    message_id = future.result()
    print(
        f"Message {message_id} sent to dead-letter topic {dead_letter_topic_id}."
    )
    return message_id


if __name__ == "__main__":
    # This block is for demonstration and will not be executed in the test environment.
    DLQ_TOPIC_ID = os.getenv("PUB_SUB_DLQ_TOPIC_ID", "dead-letter-topic")
    message_data = '{"payload": "corrupted-data"}'
    error_attributes = {"error": "JSONDecodeError", "service": "data-processor"}
    send_to_dead_letter_queue(DLQ_TOPIC_ID, message_data, error_attributes)
