import json

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client
from messaging_models import build_result, normalize_message


def batch_publish(payload, config=None):
    config = load_config(config)
    client = publisher_client(config)
    topic = config["topic_path"]
    futures = []
    for item in payload.get("messages", []):
        normalized = normalize_message(item.get("event", item))
        data = json.dumps(normalized).encode("utf-8")
        futures.append(client.publish(topic, data, **item.get("attributes", {})))
    message_ids = [future.result() for future in futures]
    return build_result(message_ids=message_ids, count=len(message_ids))
