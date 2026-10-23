import json

from google.cloud import pubsub_v1

from messaging_client import get_pubsub_client


def batch_publish(payloads, config=None):
    config = config or {}
    client = get_pubsub_client(config["project_id"])
    topic = client.topic_path(config["project_id"], config["topic_id"])
    futures = [client.publish(topic, json.dumps(payload).encode("utf-8")) for payload in payloads]
    message_ids = [future.result(timeout=30) for future in futures]
    return {"message_ids": message_ids}