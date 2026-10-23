import json
import os
from messaging_client import get_publisher_client
from messaging_models import EventMessage

TOPIC_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID")


def publish_event(event: EventMessage):
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT_ID"), TOPIC_ID)
    data = json.dumps(event.data).encode("utf-8")
    future = publisher.publish(topic_path, data, **(event.attributes or {}))
    return future.result()
