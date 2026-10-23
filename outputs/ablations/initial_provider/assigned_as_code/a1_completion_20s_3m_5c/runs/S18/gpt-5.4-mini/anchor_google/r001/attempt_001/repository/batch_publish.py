import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher_config
from messaging_models import normalize_batch_items


def batch_publish(payload, config=None):
    config = get_publisher_config(config or {})
    client = pubsub_v1.PublisherClient()
    topic = client.topic_path(config["project_id"], config["topic_id"])
    items = normalize_batch_items(payload["messages"])
    futures = []
    for item in items:
        futures.append(client.publish(topic, json.dumps(item["event"]).encode("utf-8"), message_id=item.get("message_id", ""), source=item.get("source", "batch")))
    try:
        return {"message_ids": [future.result(timeout=30) for future in futures]}
    finally:
        client.stop()
