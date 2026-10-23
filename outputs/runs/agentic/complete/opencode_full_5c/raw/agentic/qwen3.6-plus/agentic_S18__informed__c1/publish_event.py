import os
import json
from google.cloud import pubsub_v1


PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "default-project")
TOPIC_ID = os.environ.get("GOOGLE_PUBSUB_TOPIC_ID", "events-topic")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def publish_event(event_data: dict, attributes: dict | None = None) -> str:
    payload = json.dumps(event_data).encode("utf-8")
    attrs = {k: str(v) for k, v in (attributes or {}).items()}
    future = publisher.publish(topic_path, data=payload, **attrs)
    message_id = future.result()
    return message_id
