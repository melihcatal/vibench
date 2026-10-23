import json

from google.cloud import pubsub_v1

from messaging_client import get_config, publisher_client


def batch_publish(payload, config=None):
    config = get_config(config)
    client = publisher_client()
    topic = client.topic_path(config["project_id"], config["topic_id"])
    futures = []
    for item in payload.get("messages", []):
        futures.append(client.publish(topic, json.dumps(item["event"]).encode("utf-8"), message_id=str(item.get("id", "")), **item.get("attributes", {})))
    message_ids = [future.result(timeout=30) for future in futures]
    client.stop()
    return {"message_ids": message_ids}
