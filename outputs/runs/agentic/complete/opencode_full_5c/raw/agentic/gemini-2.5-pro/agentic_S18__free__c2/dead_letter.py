import os
import json
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message, ProcessingResult


def send_to_dead_letter(
    topic_id: str, failed_message: Message, result: ProcessingResult
):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    attributes = failed_message.attributes or {}
    attributes["error_message"] = result.error_message or "Unknown error"
    attributes["original_message_id"] = result.message_id

    data = json.dumps(failed_message.data).encode("utf-8")

    future = publisher.publish(topic_path, data, **attributes)
    message_id = future.result()

    print(f"Sent message {message_id} to dead-letter topic {topic_path}")
    return message_id


if __name__ == "__main__":
    dead_letter_topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID")
    if not dead_letter_topic_id:
        raise ValueError("PUBSUB_DEAD_LETTER_TOPIC_ID environment variable not set.")

    failed_msg = Message(
        data={"payload": "invalid_data"},
        attributes={"source": "importer"},
        message_id="original-msg-123",
    )

    processing_result = ProcessingResult(
        message_id="original-msg-123", status="failed", error_message="JSONDecodeError"
    )

    send_to_dead_letter(dead_letter_topic_id, failed_msg, processing_result)
