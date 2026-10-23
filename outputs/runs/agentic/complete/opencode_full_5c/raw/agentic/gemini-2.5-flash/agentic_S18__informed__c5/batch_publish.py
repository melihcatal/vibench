import json
import os
from messaging_client import get_publisher_client, get_project_id
from messaging_models import BatchEvent


def batch_publish(topic_id: str, batch_event: BatchEvent):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        batch_event: A BatchEvent object containing a list of Event objects.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    with publisher.batch(topic_path) as batcher:
        for event in batch_event.events:
            data = event.to_json().encode("utf-8")
            attributes = event.attributes if event.attributes else {}
            batcher.publish(data, **attributes)
            print(f"Added message to batch: {event.id}")

    print(f"Batch publish completed for topic: {topic_id}")
