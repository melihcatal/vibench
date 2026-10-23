import json
from messaging_client import (
    get_publisher_client,
    get_topic_path,
    PROJECT_ID,
    TOPIC_ID,
)
from messaging_models import EventPayload


def publish_event(payload: EventPayload):
    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, PROJECT_ID, TOPIC_ID)

    data = json.dumps(payload).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
    return future.result()
