from google.cloud import pubsub_v1

from messaging_client import get_config, publisher_client


def dead_letter(payload, config=None):
    config = get_config(config)
    client = publisher_client()
    topic = client.topic_path(config["project_id"], config["dead_letter_topic_id"])
    future = client.publish(topic, payload["data"].encode("utf-8"), **payload.get("attributes", {}))
    try:
        return {"message_id": future.result(timeout=30)}
    finally:
        client.stop()
