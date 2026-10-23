from typing import Optional

from messaging_client import get_publisher_client, get_topic_path, DEAD_LETTER_TOPIC_ID

def send_to_dead_letter_queue(failed_message_data: str, error: str) -> Optional[str]:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.
    In a real scenario, this is often configured automatically on the subscription,
    but this function demonstrates manually moving a message.
    """
    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_path(DEAD_LETTER_TOPIC_ID)

    data = failed_message_data.encode("utf-8")

    future = publisher.publish(
        dead_letter_topic_path, data, processing_error=str(error)
    )

    try:
        message_id = future.result()
        print(f"Sent failed message to dead-letter topic {dead_letter_topic_path} with ID: {message_id}")
        return message_id
    except Exception as e:
        print(f"Failed to send message to dead-letter topic: {e}")
        return None
