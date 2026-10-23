import json
import os
from google.cloud import pubsub_v1
from messaging_client import load_config, topic_path, normalize_attributes
from messaging_models import to_json_bytes


def publish_event(event: dict):
    config = load_config()
    client = pubsub_v1.PublisherClient()
    future = client.publish(
        topic_path(config.project_id, config.topic_id),
        to_json_bytes(event),
        **normalize_attributes(event.get("attributes")),
    )
    return {"message_id": future.result()}


if __name__ == "__main__":
    print(
        json.dumps(
            publish_event(json.loads(os.getenv("EVENT_JSON", "{}"))), sort_keys=True
        )
    )
