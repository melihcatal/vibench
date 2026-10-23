from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage
import json

def publish_event(topic_id: str, message: PubSubMessage):
    publisher = get_publisher_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError("Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable.")
    topic_path = publisher.topic_path(project_id, topic_id)

    data = message.data.encode("utf-8")
    future = publisher.publish(topic_path, data, **(message.attributes or {}))
    print(f"Published message ID: {future.result()}")
    return future.result()
