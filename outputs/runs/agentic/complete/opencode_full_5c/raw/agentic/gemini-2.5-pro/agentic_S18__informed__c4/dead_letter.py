import json
from messaging_client import (
    get_publisher_client,
    get_topic_path,
    PROJECT_ID,
    DEAD_LETTER_TOPIC_ID,
)


def send_to_dlq(failed_message_data: bytes, attributes: dict):
    publisher = get_publisher_client()
    dlq_topic_path = get_topic_path(publisher, PROJECT_ID, DEAD_LETTER_TOPIC_ID)

    future = publisher.publish(dlq_topic_path, failed_message_data, **attributes)

    message_id = future.result()
    print(f"Message sent to DLQ with ID: {message_id}")
    return message_id
