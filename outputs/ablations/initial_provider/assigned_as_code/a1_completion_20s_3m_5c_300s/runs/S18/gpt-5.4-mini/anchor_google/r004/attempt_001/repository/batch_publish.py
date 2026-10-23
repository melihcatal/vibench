from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import build_message_data, normalize_payload


def batch_publish(payload, config=None):
    config = load_config(config)
    client = publisher_client()
    topic = topic_path(client, config["project_id"], config["topic_id"])
    messages = normalize_payload(payload).get("messages", [])
    futures = []
    for index, item in enumerate(messages):
        data = build_message_data(item)
        attrs = {}
        if isinstance(item, dict):
            attrs = {str(k): str(v) for k, v in item.get("attributes", {}).items()}
        attrs.setdefault("batch_index", str(index))
        message_id = item.get("id") if isinstance(item, dict) else index
        future = client.publish(topic, data, message_id=str(message_id), **attrs)
        futures.append(future)
    try:
        return {"message_ids": [future.result(timeout=30) for future in futures]}
    finally:
        client.stop()
