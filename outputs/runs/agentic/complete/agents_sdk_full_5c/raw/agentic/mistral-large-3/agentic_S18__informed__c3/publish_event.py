# Publishes a JSON event to Google Cloud Pub/Sub topic
from messaging_client import PubSubClient
from messaging_models import PubSubMessage, MessageAttributes
import os


def publish_event(topic: str, data: dict, attributes: dict = None) -> str:
    """Publish a single event to Google Cloud Pub/Sub."""
    client = PubSubClient()
    message = PubSubMessage(
        data=data,
        attributes=MessageAttributes(attributes=attributes or {})
    )
    message_id = client.publish_message(topic, message)
    return message_id