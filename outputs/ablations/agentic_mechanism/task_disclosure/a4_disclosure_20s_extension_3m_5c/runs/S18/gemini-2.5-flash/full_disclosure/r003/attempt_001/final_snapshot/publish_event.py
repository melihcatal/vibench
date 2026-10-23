from google.cloud import pubsub_v1
import json
import os

def publish_json_event(project_id: str, topic_id: str, message: dict) -> str:
    """Publishes a JSON message to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_json = json.dumps(message)
    message_bytes = message_json.encode("utf-8")

    future = publisher.publish(topic_path, message_bytes)
    message_id = future.result()
    return message_id
