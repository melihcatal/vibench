import os
import json
from google.cloud import pubsub_v1


def publish_event(event_data, topic_id=None):
    """Publish a JSON event to Google Cloud Pub/Sub topic."""
    if topic_id is None:
        topic_id = os.getenv("PUBSUB_TOPIC_ID", "event-topic")

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    if isinstance(event_data, dict):
        data = json.dumps(event_data).encode("utf-8")
    else:
        data = str(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return {"message_id": message_id, "topic": topic_path}
