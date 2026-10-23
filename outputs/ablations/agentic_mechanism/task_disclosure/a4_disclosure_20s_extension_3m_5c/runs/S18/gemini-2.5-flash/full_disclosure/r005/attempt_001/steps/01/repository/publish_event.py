import json
import os
from google.cloud import pubsub_v1

def publish_json_event(project_id: str, topic_id: str, message: dict) -> str:
    """Publishes a JSON message to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    data = json.dumps(message).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
    return future.result()

