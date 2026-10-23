import os
from messaging_client import get_pubsub_publisher_client
from messaging_models import DeadLetterMessage, EventMessage
import json


def send_to_dead_letter(
    dead_letter_topic_id: str, dead_letter_message: DeadLetterMessage
) -> str:
    publisher = get_pubsub_publisher_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    message_data = json.dumps(
        {
            "original_message_id": dead_letter_message.original_message.id,
            "original_message_data": dead_letter_message.original_message.data,
            "error_reason": dead_letter_message.error_reason,
            "original_attributes": dead_letter_message.original_message.attributes,
        }
    ).encode("utf-8")

    future = publisher.publish(
        dead_letter_topic_path,
        message_data,
        error_reason=dead_letter_message.error_reason,
        original_message_id=dead_letter_message.original_message.id,
    )
    message_id = future.result()
    return message_id


if __name__ == "__main__":
    pass
