# publish_event.py
"""
Same-scenario scored implementation: publish_event.py
Provides a function to publish a JSON event to a managed messaging topic.
"""

from google.cloud import pubsub_v1
from messaging_models import PubSubEvent, PubSubConfig
import json


def publish_event(config: PubSubConfig, event: PubSubEvent) -> str:
    """Publish a JSON payload to a Pub/Sub topic.

    Args:
        config (PubSubConfig): Configuration containing project ID and topic name.
        event (PubSubEvent): Event payload as a dictionary.

    Returns:
        str: The Pub/Sub message ID.
    """
    publisher = pubsub_v1.PublisherClient()
    project_id = config.project_id
    topic_name = config.topic_name
    topic_path = publisher.topic_path(project_id, topic_name)
    payload = json.dumps(event.payload).encode("utf-8")
    message_id = publisher.publish(topic_path, data=payload).result()
    return message_id
