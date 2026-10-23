import json

from google.cloud import pubsub_v1

from messaging_client import create_publisher_client, load_pubsub_config, topic_path
from messaging_models import normalize_attributes, normalize_event_payload


def batch_publish(payload, config=None):
    config = load_pubsub_config(config)
    client = create_publisher_client()
    topic = topic_path(client, config["project_id"], config["topic_id"])
    batch = payload.get("events", [])
    futures = []
    for item in batch:
        event = normalize_event_payload(item.get("event", item))
        attributes = normalize_attributes(item.get("attributes"))
        data = json.dumps(event).encode("utf-8")
        futures.append(client.publish(topic, data, **attributes))
    try:
        return {"message_ids": [future.result(timeout=30) for future in futures]}
    finally:
        client.stop()
