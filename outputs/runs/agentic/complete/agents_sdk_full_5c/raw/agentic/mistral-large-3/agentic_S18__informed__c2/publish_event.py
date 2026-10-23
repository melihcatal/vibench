"""Publish a JSON event to a managed messaging topic or queue."""
import json
from messaging_client import PubSubClient
from messaging_models import Message


def publish_event(topic: str, event: dict, attributes: dict = None) -> str:
    """Publish a JSON event to Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    message = Message(
        message_id="",  # Let Pub/Sub auto-generate
        body=json.dumps(event),
        attributes=attributes
    )
    return client.publish(topic, message)


if __name__ == "__main__":
    # Example usage for testing (not scored)
    pass