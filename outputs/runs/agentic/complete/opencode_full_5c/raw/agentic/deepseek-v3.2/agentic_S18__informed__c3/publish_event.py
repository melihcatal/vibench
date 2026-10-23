import os
import json
from google.cloud import pubsub_v1


def publish_event(topic_name, event_data):
    """Publish a JSON event to a Google Cloud Pub/Sub topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    if isinstance(event_data, dict):
        data = json.dumps(event_data).encode("utf-8")
    else:
        data = str(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return {"message_id": message_id, "topic": topic_path}
