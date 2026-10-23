import os
import json
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "default-project")
TOPIC_ID = os.environ.get("GOOGLE_PUBSUB_TOPIC_ID", "events-topic")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def batch_publish(
    events: list[dict], batch_attributes: dict | None = None
) -> list[str]:
    message_ids = []
    with publisher.batch() as batch:
        for event in events:
            payload = json.dumps(event).encode("utf-8")
            attrs = {
                "batch_id": event.get("id", "unknown"),
                **(batch_attributes or {}),
            }
            future = batch.publish(topic_path, data=payload, **attrs)
            message_ids.append(future)
    return [f.result() for f in message_ids]
