import json
import os
from messaging_client import get_publisher_client
from messaging_models import DeadLetterMessage

DEAD_LETTER_TOPIC_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_DEAD_LETTER_TOPIC_ID")


def send_to_dead_letter(dead_letter_event: DeadLetterMessage):
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(
        os.getenv("GOOGLE_CLOUD_PROJECT_ID"), DEAD_LETTER_TOPIC_ID
    )
    data = json.dumps(
        {
            "original_message_id": dead_letter_event.original_message_id,
            "error_reason": dead_letter_event.error_reason,
            "original_payload": dead_letter_event.original_payload,
        }
    ).encode("utf-8")
    future = publisher.publish(topic_path, data)
    return future.result()
