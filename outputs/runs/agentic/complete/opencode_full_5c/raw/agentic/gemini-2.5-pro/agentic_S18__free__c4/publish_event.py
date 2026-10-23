import json
from messaging_client import get_publisher_client, topic_path


def publish_event(data: dict):
    """Publishes a single JSON event to the configured Pub/Sub topic."""
    publisher = get_publisher_client()

    # Data must be a bytestring
    future = publisher.publish(topic_path, json.dumps(data).encode("utf-8"))

    return future.result()
