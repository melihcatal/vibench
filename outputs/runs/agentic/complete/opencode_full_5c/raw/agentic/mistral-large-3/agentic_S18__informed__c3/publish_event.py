from messaging_client import PubSubClient
from messaging_models import Message
import os


def publish_event(topic_id: str, data: dict, attributes: dict = None) -> str:
    """
    Publishes a JSON event to a Google Cloud Pub/Sub topic.
    """
    client = PubSubClient()
    message_id = client.publish_message(topic_id, data, attributes)
    return message_id


if __name__ == "__main__":
    topic_id = os.getenv("PUBSUB_TOPIC_ID")
    event_data = {"event_type": "user_action", "user_id": "12345", "action": "click"}
    message_id = publish_event(topic_id, event_data)
    print(f"Published message with ID: {message_id}")
