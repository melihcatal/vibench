from google.cloud import pubsub_v1

from messaging_client import load_config
from messaging_models import encode_json, load_payload


def batch_publish(payload, config=None):
    config = load_config(config)
    client = pubsub_v1.PublisherClient()
    topic = client.topic_path(config["project_id"], config["topic_id"])
    results = []
    for item in load_payload(payload).get("events", []):
        event = item.get("event", item)
        attrs = item.get("attributes", {})
        future = client.publish(topic, encode_json(event), **attrs)
        results.append(future.result(timeout=30))
    try:
        return {"message_ids": results}
    finally:
        client.stop()
