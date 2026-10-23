import json
import os
from messaging_client import get_publisher_client, get_project_id
from messaging_models import Event


def publish_event(topic_id: str, event: Event):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        event: The Event object to publish.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = event.to_json().encode("utf-8")
    attributes = event.attributes if event.attributes else {}

    future = publisher.publish(topic_path, data, **attributes)
    print(f"Published message ID: {future.result()}")
