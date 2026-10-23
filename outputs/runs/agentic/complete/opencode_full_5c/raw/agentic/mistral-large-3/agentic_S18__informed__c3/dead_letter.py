from messaging_client import PubSubClient
import os


def send_to_dead_letter(
    topic_id: str, data: dict, reason: str, attributes: dict = None
) -> str:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.
    """
    client = PubSubClient()
    attributes = attributes or {}
    attributes["dead_letter_reason"] = reason
    message_id = client.dead_letter_message(topic_id, data, attributes)
    return message_id


if __name__ == "__main__":
    dead_letter_topic_id = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID")
    event_data = {
        "event_type": "failed_processing",
        "user_id": "12345",
        "action": "click",
    }
    message_id = send_to_dead_letter(
        dead_letter_topic_id, event_data, "processing_error"
    )
    print(f"Sent message to dead-letter topic with ID: {message_id}")
