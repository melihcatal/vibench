import json

from google.cloud import pubsub_v1

from messaging_client import get_publisher_config


def dead_letter(payload, config=None):
    config = get_publisher_config(config or {})
    client = pubsub_v1.PublisherClient()
    topic = client.topic_path(config["project_id"], config["dead_letter_topic_id"])
    future = client.publish(topic, json.dumps(payload["event"]).encode("utf-8"), reason=str(payload.get("reason", "failed")))
    try:
        return {"dead_letter_message_id": future.result(timeout=30)}
    finally:
        client.stop()
