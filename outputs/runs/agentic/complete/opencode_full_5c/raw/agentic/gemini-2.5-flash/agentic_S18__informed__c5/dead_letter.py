import os
from messaging_client import get_publisher_client, get_project_id


def dead_letter_message(
    dead_letter_topic_id: str, message_data: bytes, attributes: dict = None
):
    """Sends a failed message to a dead-letter destination (Pub/Sub topic).

    Args:
        dead_letter_topic_id: The ID of the dead-letter Pub/Sub topic.
        message_data: The raw message data (bytes) of the failed message.
        attributes: Optional attributes to attach to the dead-letter message.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    if attributes is None:
        attributes = {}

    future = publisher.publish(topic_path, message_data, **attributes)
    print(f"Sent to dead-letter topic with message ID: {future.result()}")
