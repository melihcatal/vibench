import json
from messaging_client import PubSubClient


def publish_event(topic_name: str, payload: dict) -> None:
    """Publish a JSON event to the configured Pub/Sub topic.

    Args:
        topic_name: Name of the topic to publish to.
        payload: Dictionary representing the event payload.
    """
    client = PubSubClient()
    # Convert payload to JSON string
    message_body = json.dumps(payload)
    # Publish the message (provider-specific implementation inside client)
    client.publish(topic_name, message_body)
    print(f"Published event to {topic_name}")
