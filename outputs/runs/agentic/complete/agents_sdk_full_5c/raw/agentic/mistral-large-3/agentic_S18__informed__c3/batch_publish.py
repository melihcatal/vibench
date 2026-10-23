# Publishes a batch of messages to Google Cloud Pub/Sub topic
from messaging_client import PubSubClient
from messaging_models import BatchPublishRequest, PubSubMessage, MessageAttributes
from typing import List
import os


def batch_publish(topic: str, messages: List[dict], base_attributes: dict = None) -> List[str]: 
    """Publish a batch of messages to Google Cloud Pub/Sub."""
    client = PubSubClient()
    pubsub_messages = [
        PubSubMessage(
            data=msg,
            attributes=MessageAttributes(attributes=base_attributes or {})
        )
        for msg in messages
    ]
    request = BatchPublishRequest(messages=pubsub_messages, topic=topic)
    message_ids = client.publish_batch(request)
    return message_ids